import json

from llm.analysis import LLMService


def select_visual_style(state):
    # Allow user or model to pick visual style based on mood/tone
    theme_info = state.get("theme_info", "")
    script = state.get("script", "")

    #LLM call to dynamically suggest style

    llm_service = LLMService(model_temperature=0.7, json_output_required=True)

    result = llm_service.generate_visual_style(script=script, theme=theme_info)
    try:
        visual_style = json.loads(result)
        print(visual_style)
    except json.JSONDecodeError as e:
        print(e)
        visual_style = {}

    return {**state, "visual_style": visual_style}
