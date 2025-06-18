"""

This module is responsible for generating a resume of each chunk of the document, in order to be used as a heading for the chunk.

"""
import asyncio
from modules.utils.schemas import InputDocument, ResumeResponse, QuestionResponse
import logging
from config import Settings, settings
from modules.utils.llm import GeneralTasksLLM
from modules.utils.templates import GENERATE_RESUME_PROMPT_TEMPLATE, GENERATE_QUESTION_PROMPT_TEMPLATE
logging.basicConfig(level=logging.INFO)




async def generate_resume(state: InputDocument, config: Settings = settings) -> InputDocument:
    logging.info("Entering generate_resume")

    llm = GeneralTasksLLM(config)

    llm_with_structured_output = llm.with_structured_output(ResumeResponse)

    async def generate_resume_async(text: str, adjacent_texts: str) -> str:
        prompt = GENERATE_RESUME_PROMPT_TEMPLATE.format(text=text, adjacent_texts=adjacent_texts)
        response = llm_with_structured_output.invoke(prompt)
        return response.resume

    for i, chunk in enumerate(state.documents_processed[1:len(state.documents_processed) - 1]):
        chunk.metadata['resume'] = await generate_resume_async(chunk.page_content, state.documents_processed[i-1].page_content + state.documents_processed[i+1].page_content)

    state.documents_processed[0].metadata['resume'] = await generate_resume_async(state.documents_processed[0].page_content, state.documents_processed[1].page_content)
    state.documents_processed[len(state.documents_processed) - 1].metadata['resume'] = await generate_resume_async(state.documents_processed[len(state.documents_processed) - 1].page_content, state.documents_processed[len(state.documents_processed) - 2].page_content)

    return state

async def generate_question(state: InputDocument, config: Settings = settings) -> InputDocument:
    logging.info("Entering generate_question")

    llm = GeneralTasksLLM(config)

    llm_with_structured_output = llm.with_structured_output(QuestionResponse)

    async def generate_question_async(text: str, adjacent_texts: str) -> str:
        prompt = GENERATE_QUESTION_PROMPT_TEMPLATE.format(text=text, adjacent_texts=adjacent_texts)
        response = llm_with_structured_output.invoke(prompt)
        return response.question
    
    for i, chunk in enumerate(state.documents_processed[1:len(state.documents_processed) - 1]):
        chunk.metadata['question'] = await generate_question_async(chunk.page_content, state.documents_processed[i-1].page_content + state.documents_processed[i+1].page_content)

    state.documents_processed[0].metadata['question'] = await generate_question_async(state.documents_processed[0].page_content, state.documents_processed[1].page_content)
    state.documents_processed[len(state.documents_processed) - 1].metadata['question'] = await generate_question_async(state.documents_processed[len(state.documents_processed) - 1].page_content, state.documents_processed[len(state.documents_processed) - 2].page_content)

    return state
    
