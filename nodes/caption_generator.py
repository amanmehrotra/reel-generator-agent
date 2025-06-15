import json
import streamlit as st
from llm.analysis import LLMService


def generate_caption(state):
    with st.spinner("🧾 Writing Instagram caption..."):
        theme = state["selected_theme"]
        scenes = state["scenes"]
        script = ""
        for scene in scenes:
            script+=scene['scene_text'] + " "
        # Use LLM to detect theme/emotion/tone
        llm_service = LLMService()

        result = llm_service.generate_caption(theme=theme, script=script, temperature=0.8)
        # print(result)
    st.markdown("✅ Caption generated successfully!")
    return {**state, "caption": result}