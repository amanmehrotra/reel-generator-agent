# LangGraph flow definition will go here
from typing import TypedDict, List, Dict

from langgraph.constants import END
from langgraph.graph import StateGraph

from nodes import generate_subtitle
from nodes.add_music import select_music
from nodes.caption_generator import generate_caption
from nodes.edit_video import edit_video
from nodes.generate_script import generate_script_and_scenes
from nodes.generate_voiceover import generate_voiceover
from nodes.input_topic import get_user_input
from nodes.return_output_video import output_result
from nodes.router import router_node
from nodes.topic_analyzer import analyze_topic
from nodes.visual_generator import generate_visuals
from nodes.visual_style_selector import select_visual_style
from nodes.generate_subtitle import generate_subtitles


class Scene(TypedDict):
    scene_text: str
    tag: str
    visual_keywords: List[str]

class ThemeInfo(TypedDict):
    theme: str
    purpose: str
    tone: str

class VisualStyle(TypedDict):
    style_name: str
    color_tone: str
    transition_type: str

class ReelState(TypedDict):
    user_input: str
    action: str
    step: str
    theme_info: List[ThemeInfo]
    selected_theme: str
    selected_purpose: str
    selected_tone: str
    script: str
    scenes: List[Scene]
    voiceover_paths: List[str]
    visual_style: VisualStyle
    visuals: List[str]
    music: str
    final_video: str
    subtitles: List
    caption: str
    unique_id: str

def run_graph():
    builder = StateGraph(ReelState)

    # Add Nodes
    builder.add_node("router", router_node)
    builder.add_node("UserInput", get_user_input)
    builder.add_node("TopicAnalyzer", analyze_topic)
    builder.add_node("ScriptAndScenes", generate_script_and_scenes)
    builder.add_node("VoiceoverCreator", generate_voiceover)
    builder.add_node("CaptionGenerator", generate_caption)
    # builder.add_node("VisualStyleSelector", select_visual_style)
    builder.add_node("VisualGenerator", generate_visuals)
    # builder.add_node("MusicSelector", select_music)
    builder.add_node("SubtitleGenerator", generate_subtitles)
    builder.add_node("VideoEditor", edit_video)
    builder.add_node("OutputResult", output_result)

    # Connect Nodes
    builder.set_entry_point("router")
    builder.add_conditional_edges("router", lambda state: router_node(state)["action"])
    builder.add_edge("UserInput", "TopicAnalyzer")
    # builder.add_edge("TopicAnalyzer", "ScriptAndScenes")
    builder.add_edge("ScriptAndScenes", "VoiceoverCreator")
    # builder.add_edge("VoiceoverCreator", "VisualStyleSelector")
    builder.add_edge("VoiceoverCreator", "VisualGenerator")
    builder.add_edge("VisualGenerator", "SubtitleGenerator")
    builder.add_edge("SubtitleGenerator", "VideoEditor")
    builder.add_edge("VideoEditor", "CaptionGenerator")
    builder.add_edge("CaptionGenerator", "OutputResult")
    builder.add_edge("OutputResult", END)

    graph = builder.compile()
    return graph
reel_graph = run_graph()