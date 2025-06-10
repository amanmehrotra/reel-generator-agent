import streamlit as st

# OpenAI variables
llm_baseurl = "https://api.groq.com/openai/v1"
llm_key = st.secrets["GROQ_API_KEY"]
llm_model = "llama-3.3-70b-versatile"

# Pixels variables
PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
PEXELS_VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"

#ElevenLabs
ELEVEN_LAB_KEY = st.secrets["ELEVEN_LAB_KEY"]
