# generate_script.py implementation
import json
import uuid
import streamlit as st
from llm.analysis import LLMService
from nodes.edit_video import edit_video
from nodes.generate_subtitle import generate_subtitles
from nodes.generate_voiceover import generate_voiceover
from nodes.visual_generator import generate_visuals

def generate_script_and_scenes(state):
    # Call LLM with theme_info + user_input to generate full script & scene split
    with st.spinner("🎬 Generating script..."):
        theme = state["selected_theme"]
        purpose = state["selected_purpose"]
        tone = state["selected_tone"]
        # Use LLM to detect theme/emotion/tone
        llm_service = LLMService()

        result = llm_service.generate_script(theme = theme, purpose = purpose, tone = tone, temperature = 0.9)
        try:
            parsed = json.loads(result)
            print(parsed)
            # script = parsed.get("script", "")
            scenes = parsed.get("scenes", [])
            print(scenes)
        except json.JSONDecodeError:
            script = "Unable to parse script. Please revise model output."
            scenes = []
    st.markdown("✅ Script generated successfully!")
    return {**state, "scenes": scenes, "unique_id": uuid.uuid4().hex[:8]}

# if __name__ == "__main__":
#     state = generate_script_and_scenes({
#         "user_input": "Doubt kills more dreams than failure ever will.",
#         "theme_info": "Let it go, or it will keep you stuck"
#     })
#     state = generate_voiceover(state)
#     # state = select_visual_style(state)
#     state = generate_visuals(state)
#     state = generate_subtitles(state)
#     # state = {'user_input': 'Doubt kills more dreams than failure ever will.', 'theme_info': 'Sacrifice now, shine later', 'script': '', 'scenes': [{'scene_text': "You've been on the sidelines of your own life, waiting for permission to start.", 'tag': 'hook', 'visual_keywords': ['silhouette at sunset', 'frozen in thought']}, {'scene_text': "You've been stuck in the cycle of self-doubt, afraid to take the leap.", 'tag': 'build_up', 'visual_keywords': ['nighttime cityscape', 'lost in reflection']}, {'scene_text': 'But what if the sacrifice you make today is the bridge to your dream tomorrow? What if the struggle is the catalyst for your strength?', 'tag': 'breakthrough', 'visual_keywords': ['running through mist', 'unfurling wings']}, {'scene_text': 'So, take the leap. Make the sacrifice. Shine later.', 'tag': 'final_impact', 'visual_keywords': ['soaring eagle', 'golden sunrise']}], 'voiceover_paths': ['../assets/voiceovers\\voiceover_scene_0_8252c21c.mp3', '../assets/voiceovers\\voiceover_scene_1_f4861066.mp3', '../assets/voiceovers\\voiceover_scene_2_62a764a0.mp3', '../assets/voiceovers\\voiceover_scene_3_a9622d60.mp3'], 'visuals': ['../assets/visuals\\scene_0_cbc77988.mp4', '../assets/visuals\\scene_1_d36c5321.mp4', '../assets/visuals\\scene_2_361c9b1b.mp4', '../assets/visuals\\scene_3_185baa03.mp4'], 'subtitles': [{'text': " You've been on the sidelines of your own life, waiting for permission to start.", 'task': 'transcribe', 'language': 'English', 'duration': 5.38, 'words': [{'word': "You've", 'start': 0.04, 'end': 0.3}, {'word': 'been', 'start': 0.3, 'end': 0.48}, {'word': 'on', 'start': 0.48, 'end': 0.62}, {'word': 'the', 'start': 0.62, 'end': 0.74}, {'word': 'sidelines', 'start': 0.74, 'end': 1.36}, {'word': 'of', 'start': 1.36, 'end': 1.58}, {'word': 'your', 'start': 1.58, 'end': 1.72}, {'word': 'own', 'start': 1.72, 'end': 1.92}, {'word': 'life,', 'start': 1.92, 'end': 2.7}, {'word': 'waiting', 'start': 2.7, 'end': 3.14}, {'word': 'for', 'start': 3.14, 'end': 3.74}, {'word': 'permission', 'start': 3.74, 'end': 4.16}, {'word': 'to', 'start': 4.16, 'end': 4.44}, {'word': 'start.', 'start': 4.44, 'end': 4.84}], 'segments': [{'id': 0, 'seek': 0, 'start': 0, 'end': 5.36, 'text': " You've been on the sidelines of your own life, waiting for permission to start.", 'tokens': [50365, 509, 600, 668, 322, 264, 20822, 9173, 295, 428, 1065, 993, 11, 3806, 337, 11226, 281, 722, 13, 50633], 'temperature': 0, 'avg_logprob': 0.736979, 'compression_ratio': 1.0394737, 'no_speech_prob': 8.865848e-12}], 'x_groq': {'id': 'req_01jx7r9dbde7w9xzxdte2khz1k'}}, {'text': " You've been stuck in the cycle of self-doubt, afraid to take the leap.", 'task': 'transcribe', 'language': 'English', 'duration': 5.04, 'words': [{'word': "You've", 'start': 0, 'end': 0.26}, {'word': 'been', 'start': 0.26, 'end': 0.44}, {'word': 'stuck', 'start': 0.44, 'end': 0.82}, {'word': 'in', 'start': 0.82, 'end': 1.04}, {'word': 'the', 'start': 1.04, 'end': 1.16}, {'word': 'cycle', 'start': 1.16, 'end': 1.48}, {'word': 'of', 'start': 1.48, 'end': 1.7}, {'word': 'self-doubt,', 'start': 1.7, 'end': 2.74}, {'word': 'afraid', 'start': 2.74, 'end': 3.38}, {'word': 'to', 'start': 3.38, 'end': 3.92}, {'word': 'take', 'start': 3.92, 'end': 4.14}, {'word': 'the', 'start': 4.14, 'end': 4.34}, {'word': 'leap.', 'start': 4.34, 'end': 4.76}], 'segments': [{'id': 0, 'seek': 0, 'start': 0, 'end': 5.04, 'text': " You've been stuck in the cycle of self-doubt, afraid to take the leap.", 'tokens': [50365, 509, 600, 668, 5541, 294, 264, 6586, 295, 2698, 12, 67, 26705, 11, 4638, 281, 747, 264, 19438, 13, 50617], 'temperature': 0, 'avg_logprob': 0.8234744, 'compression_ratio': 0.9722222, 'no_speech_prob': 7.43948e-12}], 'x_groq': {'id': 'req_01jx7r9getedza5bsztcve8a5k'}}, {'text': ' But what if the sacrifice you make today is the bridge to your dream tomorrow? What if the struggle is the catalyst for your strength?', 'task': 'transcribe', 'language': 'English', 'duration': 9.97, 'words': [{'word': 'But', 'start': 0, 'end': 0.18}, {'word': 'what', 'start': 0.18, 'end': 0.38}, {'word': 'if', 'start': 0.38, 'end': 0.58}, {'word': 'the', 'start': 0.58, 'end': 0.76}, {'word': 'sacrifice', 'start': 0.76, 'end': 1.26}, {'word': 'you', 'start': 1.26, 'end': 1.74}, {'word': 'make', 'start': 1.74, 'end': 1.96}, {'word': 'today', 'start': 1.96, 'end': 2.36}, {'word': 'is', 'start': 2.36, 'end': 3.18}, {'word': 'the', 'start': 3.18, 'end': 3.32}, {'word': 'bridge', 'start': 3.32, 'end': 3.74}, {'word': 'to', 'start': 3.74, 'end': 4.06}, {'word': 'your', 'start': 4.06, 'end': 4.22}, {'word': 'dream', 'start': 4.22, 'end': 4.66}, {'word': 'tomorrow?', 'start': 4.66, 'end': 5.26}, {'word': 'What', 'start': 5.58, 'end': 6.22}, {'word': 'if', 'start': 6.22, 'end': 6.4}, {'word': 'the', 'start': 6.4, 'end': 6.56}, {'word': 'struggle', 'start': 6.56, 'end': 7}, {'word': 'is', 'start': 7, 'end': 7.46}, {'word': 'the', 'start': 7.46, 'end': 7.6}, {'word': 'catalyst', 'start': 7.6, 'end': 8.06}, {'word': 'for', 'start': 8.06, 'end': 8.68}, {'word': 'your', 'start': 8.68, 'end': 8.9}, {'word': 'strength?', 'start': 8.9, 'end': 9.68}], 'segments': [{'id': 0, 'seek': 0, 'start': 0, 'end': 6, 'text': ' But what if the sacrifice you make today is the bridge to your dream tomorrow?', 'tokens': [50365, 583, 437, 498, 264, 11521, 291, 652, 965, 307, 264, 7283, 281, 428, 3055, 4153, 30, 50665], 'temperature': 0, 'avg_logprob': 0.8298323, 'compression_ratio': 1.3267326, 'no_speech_prob': 8.718197e-12}, {'id': 1, 'seek': 0, 'start': 6, 'end': 10, 'text': ' What if the struggle is the catalyst for your strength?', 'tokens': [50665, 708, 498, 264, 7799, 307, 264, 23868, 337, 428, 3800, 30, 50865], 'temperature': 0, 'avg_logprob': 0.8298323, 'compression_ratio': 1.3267326, 'no_speech_prob': 8.718197e-12}], 'x_groq': {'id': 'req_01jx7r9pw5ee29k9vznrkhctqr'}}, {'text': ' So take the leap, make the sacrifice, shine later.', 'task': 'transcribe', 'language': 'English', 'duration': 5.5600000000000005, 'words': [{'word': 'So', 'start': 0.02, 'end': 0.24}, {'word': 'take', 'start': 0.24, 'end': 1.16}, {'word': 'the', 'start': 1.16, 'end': 1.44}, {'word': 'leap,', 'start': 1.44, 'end': 2.1}, {'word': 'make', 'start': 2.1, 'end': 2.68}, {'word': 'the', 'start': 2.68, 'end': 2.98}, {'word': 'sacrifice,', 'start': 2.98, 'end': 4.34}, {'word': 'shine', 'start': 4.34, 'end': 4.58}, {'word': 'later.', 'start': 4.58, 'end': 4.98}], 'segments': [{'id': 0, 'seek': 0, 'start': 0, 'end': 5.04, 'text': ' So take the leap, make the sacrifice, shine later.', 'tokens': [50365, 407, 747, 264, 19438, 11, 652, 264, 11521, 11, 12207, 1780, 13, 50617], 'temperature': 0, 'avg_logprob': 0.6687114, 'compression_ratio': 1, 'no_speech_prob': 7.973791e-12}], 'x_groq': {'id': 'req_01jx7ra23he5xrf422xpbgwrvm'}}]}
#     edit_video(state)
#     # state = generate_subtitles(state)

