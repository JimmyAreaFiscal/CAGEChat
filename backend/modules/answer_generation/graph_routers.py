from backend.modules.utils.schemas import AgentState

def on_topic_router(state: AgentState) -> AgentState:
    print("Entering on_topic_router")
    on_topic = state.get('on_topic', 'Não').strip().lower() 
    if on_topic == 'sim':
        print("on_topic_router: Question is on topic, routing to retrieve")
        return "retrieve"
    else:
        print("on_topic_router: Question is not on topic, routing to off_topic_response")
        return "off_topic_response"
    

def proceed_router(state: AgentState):
    print("Entering proceed_router")
    rephrase_count = state.get('rephrase_count', 0)
    if state.get('proceed_to_generate', False):
        print("Routing to generate_answer")
        return "generate_answer"
    elif rephrase_count >= 2:
        print("Maximum rephrasing attempts reached, routing to cannot_answer")
        return "cannot_answer"
    else:
        print("Routing to refine_question")
        return "refine_question"