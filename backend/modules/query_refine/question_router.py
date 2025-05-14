"""

This module is responsible for routing the question to the correct node.

"""

from backend.modules.utils.schemas import AgentState


def on_topic_router(state: AgentState) -> AgentState:
    print("Entering on_topic_router")
    on_topic = state.get('on_topic', 'Não').strip().lower() 
    if on_topic == 'sim':
        print("on_topic_router: Question is on topic, routing to question_decomposition")
        return "question_decomposition"
    else:
        print("on_topic_router: Question is not on topic, routing to off_topic_response")
        return "off_topic_response"

