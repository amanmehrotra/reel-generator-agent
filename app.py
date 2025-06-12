# Streamlit UI will go here
import glob
import os
import uuid

import streamlit as st
from streamlit import session_state

from flow import run_graph, reel_graph


def start():

# Page config
    st.set_page_config(page_title="Reel Generator Agent", layout="wide")
### remove deploy button

    # st.markdown("""
    #     <style>
    #         /* Hide top toolbar including 'Deploy', 'Settings', 'Feedback' */
    #         [data-testid="stToolbar"] {
    #             display: none;
    #         }
    #
    #         /* Optionally hide the footer (Streamlit branding) */
    #         footer {
    #             visibility: hidden;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)
    # Header
    st.title("AM0003- Reel Generator Agent")

    topic_options = [
        { "label": "Heartbreak & Healing", "value": "heartbreak" },
        { "label": "Discipline & Consistency", "value": "discipline" },
        { "label": "Loneliness & Inner Strength", "value": "loneliness" },
        { "label": "Spiritual Growth", "value": "spiritual_growth" },
        { "label": "Self-Worth & Confidence", "value": "self_worth" },
        { "label": "Overthinking & Mental Peace", "value": "overthinking" },
        { "label": "Comeback from Failure", "value": "comeback" },
        { "label": "Fear & Courage", "value": "fear" },
        { "label": "Toxic People & Letting Go", "value": "toxic_people" },
        { "label": "Gratitude & Abundance", "value": "gratitude" },
        { "label": "Focus & Productivity", "value": "focus" },
        { "label": "Chasing Dreams", "value": "dreams" },
        { "label": "Self-Love", "value": "self_love" },
        { "label": "Purpose & Meaning", "value": "purpose" },
        { "label": "Comparison & Self-Acceptance", "value": "comparison" }
]

    if 'motivational_topic' not in session_state:
        st.session_state.motivational_topic = None
    if 'themes' not in session_state:
        st.session_state.themes = []
    if 'theme_options' not in session_state:
        st.session_state.theme_options = []
    if 'selected_theme' not in session_state:
        st.session_state.selected_theme = None
    if 'selected_purpose' not in session_state:
        st.session_state.selected_purpose = None
    if 'selected_tone' not in session_state:
        st.session_state.selected_tone = None
    if 'graph_state' not in session_state:
        st.session_state.graph_state = None
    if 'caption' not in session_state:
        st.session_state.caption = None
    if 'file_path' not in session_state:
        st.session_state.file_path = None
    if 'unique_id' not in session_state:
        st.session_state.unique_id = None

    # Sidebar: topic Selection
    motivational_topic = st.sidebar.selectbox(
        "Select Type",
         [option["label"] for option in topic_options],
        index=0
    )
    st.session_state.motivational_topic = motivational_topic
    # print(session_state.motivational_topic)
    # Fetch Button
    analyze_button = st.sidebar.button("Submit")
    if analyze_button:
        with st.spinner("Generating themes, please wait..."):
            st.session_state.caption = None
            st.session_state.final_path = None
            st.session_state.unique_id = None
            result = reel_graph.invoke({"user_input": motivational_topic,
                                        "step": ""})
            st.session_state.graph_state = result
            themes = result['theme_info']['themes']
            st.session_state.themes = themes
            st.session_state.theme_options = [option["theme"] for option in themes]
    if st.session_state.theme_options:
        st.session_state.selected_theme = st.selectbox("Select Theme", st.session_state.theme_options, index=0)
        st.session_state.selected_purpose, st.session_state.selected_tone = next(
            ((opt["purpose"], opt["tone"]) for opt in st.session_state.themes if opt["theme"] == st.session_state.selected_theme), None)


        submit_button = st.button("Generate reel")
        if submit_button:
            st.session_state.caption = None
            st.session_state.final_path = None
            st.session_state.unique_id = None
            print(st.session_state.selected_theme, st.session_state.selected_purpose, st.session_state.selected_tone)
            prev_state = st.session_state.graph_state
            prev_state['step'] = 'ScriptAndScenes'
            prev_state['selected_theme'] = st.session_state.selected_theme
            prev_state['selected_purpose'] = st.session_state.selected_purpose
            prev_state['selected_tone'] = st.session_state.selected_tone
            reel_result = reel_graph.invoke(prev_state)
            st.session_state.caption = reel_result['caption']
            st.session_state.unique_id = reel_result['unique_id']
            #print(reel_result)
    if st.session_state.caption:
        st.markdown(f'Caption: {st.session_state.caption}')
    if st.session_state.file_path:
        with open(st.session_state.file_path,"rb") as f:
            video_bytes = f.read()
            st.download_button(
                label="📥 Download Your Video",
                data=video_bytes,
                file_name=f"video_{uuid.uuid4()}.mp4",
                mime="video/mp4"
        )
        if st.button('Clean associated files'):
            delete_files_with_suffix('./assets/voiceovers', st.session_state.unique_id)
            delete_files_with_suffix('./assets/visuals', st.session_state.unique_id)
            if st.session_state.file_path is not None and os.path.exists(st.session_state.final_path):
                os.remove(st.session_state.file_path)

def delete_files_with_suffix(directory, unique_id):
    # Pattern: match any file ending with the unique_id
    pattern_mp3 = os.path.join(directory, f"*_{unique_id}.mp3")
    pattern_mp4 = os.path.join(directory, f"*_{unique_id}.mp4")

    for pattern in [pattern_mp3, pattern_mp4]:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")