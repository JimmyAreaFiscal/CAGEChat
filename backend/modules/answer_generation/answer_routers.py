from backend.modules.utils.schemas import AgentState
import logging

logging.basicConfig(level=logging.INFO)



def proceed_to_answer_router(state: AgentState) -> str:
    logging.info("Entering proceed_to_answer_router")
    
    if state.get('qa_context', None):
        logging.info("Routing to generate_answer")
        return "generate_answer"
    else:
        logging.info("Routing to cannot_answer")
        return "cannot_answer"
    