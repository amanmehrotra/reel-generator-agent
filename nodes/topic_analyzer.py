import json
from json import JSONDecodeError

from llm.analysis import LLMService

def analyze_topic(state):
    motivational_topic = state["user_input"]
    # Use LLM to detect theme/emotion/tone
    llm_service = LLMService()

    result = llm_service.analyze_topic(user_input=motivational_topic, temperature=0.7)
    print(result)
    try:
        parsed = json.loads(result)
    except JSONDecodeError as e:
        raise e
    # print(parsed)
    return {**state, "theme_info": parsed}

# if __name__ == "__main__":
#     analyze_topic({"user_input": "Chasing Dreams"})