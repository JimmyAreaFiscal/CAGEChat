from modules.utils.schemas import AgentState
import logging
from config import Settings, settings
logging.basicConfig(level=logging.INFO)



def proceed_to_answer_router(state: AgentState, config: Settings = settings) -> str:
    logging.info("Entering proceed_to_answer_router")
    
    if state.get('qa_context', None):
        logging.info("Routing to generate_answer")
        return "generate_answer"
    else:
        logging.info("Routing to cannot_answer")
        return "cannot_answer"
    