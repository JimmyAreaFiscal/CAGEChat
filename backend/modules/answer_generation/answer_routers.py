from backend.modules.utils.schemas import AgentState



def proceed_to_answer_router(state: AgentState) -> str:
    print("Entering proceed_to_answer_router")
    
    if state.get('qa_context', None):
        print("Routing to generate_answer")
        return "generate_answer"
    else:
        print("Routing to cannot_answer")
        return "cannot_answer"
    