import logging

from backend.modules.utils.schemas import RetrievalState

logging.basicConfig(level=logging.INFO)

def proceed_retrieval_router(state: RetrievalState):
    logging.info("Entering proceed_retrieval_router")
    rephrase_count = state.get('rephrase_count', 0)
    if state.get('proceed_to_generate', False):
        logging.info("Routing to generate_retrieval_answer")
        return "generate_retrieval_answer"
    
    elif rephrase_count >= 2:
        logging.info("Maximum rephrasing attempts reached, routing to cannot_answer_retrieval_task")
        return "cannot_answer_retrieval_task"
    
    else:
        logging.info("Routing to refine_question")
        return "refine_question"