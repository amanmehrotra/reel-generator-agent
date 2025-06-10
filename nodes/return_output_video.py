import glob
import os
import uuid

import streamlit as st
def output_result(state):
    print(state)
    print(f"Video created at: {state['final_video']}")
    output_path = state['final_video']
    # Step 2: Show download button

    with open(output_path, "rb") as file:
        st.session_state.video_bytes = file.read()
    return state