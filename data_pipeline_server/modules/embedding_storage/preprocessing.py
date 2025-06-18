"""

This module is responsible for preprocessing and routing the document before it is chunked and embedded.

"""
from modules.utils.schemas import InputDocument, DocumentTypeResponse
import logging
from config import Settings, settings
from modules.utils.llm import GeneralTasksLLM
from modules.utils.templates import VERIFY_DOCUMENT_TYPE_PROMPT_TEMPLATE
logging.basicConfig(level=logging.INFO)




def verify_document_type(state: InputDocument, config: Settings = settings) -> str:
    logging.info("Entering verify_document_type")

    llm = GeneralTasksLLM(config)

    llm_with_structured_output = llm.with_structured_output(DocumentTypeResponse)
    prompt = VERIFY_DOCUMENT_TYPE_PROMPT_TEMPLATE.format(group=state.group, title=state.title, allowed_document_types=config.DocumentTypeSettings.ALLOWED_DOCUMENT_TYPES)

    response = llm_with_structured_output.invoke(prompt)

    state.document_type = response.document_type

    return state


def document_type_router(state: InputDocument, config: Settings = settings) -> str:
    logging.info("Entering document_type_router")
    
    if state.document_type:
        if state.document_type == 'legislação':
            return "chunking_by_article"
        elif state.document_type == 'manuais e guias':
            return "chunking_by_chapter"
        elif state.document_type == 'outros':
            return "semantic_chunking"
        else:
            raise ValueError("Document type not found")
    else:
        raise ValueError("Document type not found")