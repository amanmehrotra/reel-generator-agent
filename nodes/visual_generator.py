import os
import shutil
import uuid

import requests

from utils.config import PEXELS_VIDEO_SEARCH_URL, PEXELS_API_KEY
import streamlit as st

def generate_visual_with_pexels(query):
    headers = {
        "Authorization": f"{PEXELS_API_KEY}"
    }
    params = {
        "query": query,
        "orientation": "portrait",
        "size": "large",
        "per_page": 1
    }

    try:
        response = requests.get(PEXELS_VIDEO_SEARCH_URL, headers=headers, params=params)
        data = response.json()
        #print(data)
        video_url = None
        if data["videos"]:
            video_files = data["videos"][0]["video_files"]
            video_url = None
            for file in video_files:
                if file['quality'] == 'uhd':
                    video_url = file['link']
            if video_url is None:
                video_url = data["videos"][0]["video_files"][0]["link"]
        return video_url  # Ensure this is the correct key from the response
    except Exception as e:
        print(f"[PixelBy Error] Failed to generate video: {e}")
        return None

def download_video(video_url, filename):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return filename
    except Exception as e:
        print(f"[Download Error] Failed to download video: {e}")
        return None


def generate_visuals(state):
    with st.spinner("🎬 Generating visuals..."):
        output_dir = "./assets/visuals"
        scenes = state.get("scenes", [])
        visual_style = state.get("visual_style", {}).get("style_name", "default")
        os.makedirs(output_dir, exist_ok=True)
        visual_paths = []
        visual_id = state['unique_id']
        for i, scene in enumerate(scenes):
            keywords = scene.get("visual_keywords", [])
            # Combine keywords and style to form a dummy visual asset name
            # prompt = "_".join([kw.replace(" ", "-") for kw in keywords[:2]])
            query = keywords[0]+" "+"4K"
            video_url = generate_visual_with_pexels(query)
            # visual_id = uuid.uuid4().hex[:8]
            filename = os.path.join(output_dir, f"scene_{i}_{visual_id}.mp4")

            if video_url:
                saved_path = download_video(video_url, filename)
                visual_paths.append(saved_path if saved_path else f"{output_dir}/placeholder_scene_{i}.mp4")
            else:
                visual_paths.append(f"{output_dir}/placeholder_scene_{i}.mp4")
        print(visual_paths)
    st.markdown("✅ Visuals generated successfully!")
    return {**state, "visuals": visual_paths}
