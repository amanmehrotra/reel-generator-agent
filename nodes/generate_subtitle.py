import json
import uuid
import os
from groq import Groq

from utils.config import llm_key

import streamlit as st
def generate_subtitles(state):
    with st.spinner("📝 Generating subtitles..."):
        # Initialize the Groq client
        client = Groq(
            api_key=llm_key,
        )
        subtitles = []
        voiceover_paths = state["voiceover_paths"]
        for filename in voiceover_paths:
        # Specify the path to the audio file

        # Open the audio file
            with open(filename, "rb") as file:
                # Create a transcription of the audio file
                transcription = client.audio.transcriptions.create(
                    file=file,  # Required audio file
                    model="whisper-large-v3-turbo",  # Required model to use for transcription
                    prompt="Specify context or spelling",  # Optional
                    response_format="verbose_json",  # Optional
                    timestamp_granularities=["word", "segment"],
                    # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
                    language="en",  # Optional
                    temperature=0.0  # Optional
                )
                subtitles.append(transcription.to_dict())
    st.markdown("✅ Subtitles generated successfully!")
    # print(subtitles)
    return {**state, "subtitles": subtitles}
# def generate_subtitles(state):
#     """
#     Generate subtitles from scene script.
#     Output format:
#     [
#         {
#             "text": "Your scene line here",
#             "style": {
#                 "font": "Arial-Bold",
#                 "color": "white",
#                 "position": "bottom"
#             }
#         },
#         ...
#     ]
#     """
#     scenes = state.get("scenes", [])
#     subtitles = []
#
#     for scene in scenes:
#         subtitles.append({
#             "text": scene["scene_text"],
#             "style": {
#                 "font": "Arial",
#                 "color": "white",
#                 "position": "bottom"
#             }
#         })
#
#     return {**state, "subtitles": subtitles}
