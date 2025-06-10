# generate_voiceover.py implementation
import os
import uuid

from elevenlabs import ElevenLabs
from gtts import gTTS

from utils.config import ELEVEN_LAB_KEY

import streamlit as st
def generate_voiceover(state):
    with st.spinner("🎙️ Generating voiceover..."):
        scenes = state.get("scenes", [])
        output_dir = "./assets/voiceovers"
        os.makedirs(output_dir, exist_ok=True)
        # Placeholder logic: Normally you’d call a TTS API here for each scene_text
        voiceover_paths = []
        unique_id = state['unique_id']
        for i, scene in enumerate(scenes):
            scene_text = scene.get("scene_text", f"Scene {i}")
            # unique_id = uuid.uuid4().hex[:8]
            filename = f"voiceover_scene_{i}_{unique_id}.mp3"
            filepath = os.path.join(output_dir, filename)

            print(f"[TTS] Generating voiceover for scene: {scene_text}")
            #Call TTS API like Google TTS or ElevenLabs to generate MP3 for each scene_text
            client = ElevenLabs(
                api_key=ELEVEN_LAB_KEY,
            )
            audio = client.text_to_speech.convert(
                voice_id="L1aJrPa7pLJEyYlh3Ilq",
                output_format="mp3_44100_128",
                text=scene_text,
                model_id="eleven_turbo_v2_5",
                # voice_settings={
                #     "stability": 0.35,
                #     "similarity_boost": 0.85
                # }
            )

            with open(filepath, "wb") as f:
                for chunk in audio:
                    if isinstance(chunk, bytes):
                        f.write(chunk)
            # tts = gTTS(text=scene_text, lang='en')
            # tts.save(filepath)
            voiceover_paths.append(filepath)
    st.markdown("✅ Voiceover generated successfully!")
    return {**state, "voiceover_paths": voiceover_paths}