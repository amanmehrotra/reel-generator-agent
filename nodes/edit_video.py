# edit_video.py implementation
import os
import tempfile

from moviepy import concatenate_videoclips, VideoFileClip, AudioFileClip, CompositeAudioClip, vfx, TextClip, \
    CompositeVideoClip, ColorClip

from uuid import uuid4
import streamlit as st

def edit_video(state):
    with st.spinner("🎞️ Creating video..."):
        # print(state)
        visual_paths = state.get("visuals", [])             # List of MP4s
        voiceover_paths = state.get("voiceover_paths", [])       # List of MP3s
        background_music_path = state.get("music")  # Single MP3

        output_dir = "./final_videos"
        os.makedirs(output_dir, exist_ok=True)
        target_clip = VideoFileClip(visual_paths[2])
        # print(target_clip.size)
        target_resolution = (1080,1920)
        target_clip.close()
        video_clips = []
        audio_clips = []
        subtitle_clips = []
        current_start = 0.0
        subtitles = state.get("subtitles", [])
        for i, (visual_path, voiceover_path) in enumerate(zip(visual_paths, voiceover_paths)):
            try:
                video_clip = VideoFileClip(visual_path)
                voiceover_clip = AudioFileClip(voiceover_path)

                # Trim or extend video to match voiceover duration
                duration = voiceover_clip.duration
                if video_clip.duration > duration:
                    video_clip = video_clip.subclipped(0, duration)
                else:
                    video_clip = video_clip.with_duration(duration)

                if video_clip.size != target_resolution:
                    video_clip = video_clip.with_effects([vfx.Resize(target_resolution)])

                video_clip_with_voiceover = video_clip.with_audio(voiceover_clip)
                video_clips.append(video_clip_with_voiceover)
                audio_clips.append(voiceover_clip)

                # Create subtitles using voiceover timing
                if i < len(subtitles):
                    sub = subtitles[i]
                    end_time = current_start + voiceover_clip.duration
                    chunks = chunk_words_by_timing(sub['words'])
                    print(chunks)
                    for item in chunks:
                        current_per_subtitle_start = current_start+ item['start']
                        txt_clip = TextClip(
                            text=item["word"],
                            font_size=75,
                            font="./assets/fonts/BebasNeue-Regular.ttf",
                            color="white",
                            stroke_color="black",
                            stroke_width=2,
                            method="caption",
                            size=((video_clip.w-80)//2*2, 88)
                        )
                        # padded_clip = txt_clip.with_background_color(
                        #     size=(video_clip.w, txt_clip.h+40),
                        #     color = (255,0,0),
                        #     opacity = 0,
                        #     pos=("center","center")
                        # )
                        padded_height = ((txt_clip.h + 40) // 2) * 2
                        # # Safe Y calculation: bottom margin with headroom
                        # safe_y = min(video_clip.h - padded_height - 60, video_clip.h - 200)
                        txt_clip = txt_clip.with_position(("center", video_clip.h-700)).with_start(current_per_subtitle_start).with_duration(current_start+item['end']-current_per_subtitle_start)
                        subtitle_clips.append(txt_clip)
                    current_start = end_time
            except Exception as e:
                print(f"[WARNING] Skipping scene {i}: {e}")
                continue

        if not video_clips:
            raise RuntimeError("No valid clips to assemble.")

        final_video = concatenate_videoclips(video_clips, method="compose")
        # final_audio = CompositeAudioClip(audio_clips)
        black_overlay = ColorClip(size=final_video.size, color=(0, 0, 0))
        black_overlay = black_overlay.with_opacity(0.3).with_duration(final_video.duration)
        final_video_with_subtitles = CompositeVideoClip([final_video, black_overlay] + subtitle_clips)
        # final_video_with_subtitles = final_video_with_subtitles.resized(height=(1080// 2) * 2,
        # width=(1920// 2) * 2)
        # if background_music_path:
        #     try:
        #         bg_music = AudioFileClip(background_music_path)
        #
        #         final_audio = CompositeAudioClip([final_video.audio, bg_music])
        #         final_video = final_video.set_audio(final_audio)
        #     except Exception as e:
        #         print(f"[INFO] Background music failed: {e}")

        # final_path = os.path.join(output_dir, f"motivational_reel_{uuid4()}.mp4")
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            temp_path = f.name
        # final_video_with_subtitles.show()
        log_area = st.empty()
        progress_bar = st.empty()
        status_text = st.empty()

        logger = StreamlitLogger(log_area, progress_bar, status_text)
        final_video_with_subtitles.write_videofile(temp_path,
                                                   fps=30,
                                                   codec="libx264",
                                                   audio_codec="aac",
                                                   audio_bitrate="128K",
                                                   # logger=logger,
                                                   preset="slow",
                                                   ffmpeg_params=[
                                                       "-crf", "20",  # Constant quality: visually lossless
                                                       "-movflags", "faststart", # Enables faster playback start on mobile
                                                       "-pix_fmt", "yuv420p",# Ensures wide compatibility across devices
                                                       "-profile:v", "main",# Avoids unnecessary IG compression
                                                       "-level", "4.0"  # Safe level for mobile streaming
                                                   ],
                                                   threads=4)

    st.markdown("✅ Video created successfully!")
    return {**state, "final_video": str(temp_path)}

def chunk_words_by_timing(words, max_chunk_duration=1.2):
    """
    Groups words into chunks (2–3 words) if their total duration is under max_chunk_duration.
    Returns a list of dicts with text, start, and end.
    """
    chunks = []
    current_chunk = []
    chunk_start = None
    chunk_end = None

    for word in words:
        word_text = word["word"]
        word_start = word["start"]
        word_end = word["end"]

        if not current_chunk:
            current_chunk = [word_text]
            chunk_start = word_start
            chunk_end = word_end
        else:
            duration_if_added = word_end - chunk_start
            if duration_if_added <= max_chunk_duration:
                current_chunk.append(word_text)
                chunk_end = word_end
            else:
                chunks.append({
                    "word": " ".join(current_chunk),
                    "start": chunk_start,
                    "end": chunk_end
                })
                current_chunk = [word_text]
                chunk_start = word_start
                chunk_end = word_end

    # Add the last chunk
    if current_chunk:
        chunks.append({
            "word": " ".join(current_chunk),
            "start": chunk_start,
            "end": chunk_end
        })

    return chunks

class StreamlitLogger:
    def __init__(self, log_placeholder, progress_placeholder, status_placeholder):
        self.log_placeholder = log_placeholder
        self.progress_placeholder = progress_placeholder
        self.status_placeholder = status_placeholder
        self.logs = ""

    def __call__(self, *args, **kwargs):
        message = kwargs.get("message", args[0] if args else "")
        self.logs += str(message) + "\n"
        self.log_placeholder.text_area("Logs", self.logs, height=200)

def iter_bar(self, iterable=None, **kwargs):
    # Accept the iterable from:
    # 1) positional argument 'iterable'
    # 2) keyword 'chunk' (used by MoviePy)
    # 3) keyword 'iterable' if present
    if iterable is None:
        iterable = kwargs.get("chunk") or kwargs.get("iterable")
    if iterable is None:
        print("No iterable passed to iter_bar")

    total = len(iterable)
    for i, item in enumerate(iterable):
        self.progress_placeholder.progress((i + 1) / total)
        self.status_placeholder.markdown(f"Progress: {i+1}/{total} ({int((i + 1) / total * 100)}%)")
        yield item
