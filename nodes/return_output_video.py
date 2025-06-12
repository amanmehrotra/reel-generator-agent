import glob
import os
import uuid

import streamlit as st
def output_result(state):
    print(state)
    print(f"Video created at: {state['final_video']}")
    output_path = state['final_video']
    # Step 2: Show download button

    st.session_state.file_path = output_path
    return state