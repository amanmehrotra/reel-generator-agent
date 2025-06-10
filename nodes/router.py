def router_node(state):
    action="UserInput"
    if state["step"] == "":
        action="UserInput"
    elif state["step"] == "ScriptAndScenes":
        action="ScriptAndScenes"
    return {**state, "action": action}