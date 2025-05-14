

from backend.modules.utils.schemas import RetrievalState


def proceed_retrieval_router(state: RetrievalState):
    print("Entering proceed_retrieval_router")
    rephrase_count = state.get('rephrase_count', 0)
    if state.get('proceed_to_generate', False):
        print("Routing to generate_retrieval_answer")
        return "generate_retrieval_answer"
    
    elif rephrase_count >= 2:
        print("Maximum rephrasing attempts reached, routing to cannot_answer_retrieval_task")
        return "cannot_answer_retrieval_task"
    
    else:
        print("Routing to refine_question")
        return "refine_question"