from typing import TypedDict, List, Dict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.documents import Document

State = None


class AgentState(TypedDict):
    
    messages: List[BaseMessage]
    documents: List[Document]
    agent_think: str
    on_topic: str 
    rephrased_question: str 
    proceed_to_generate: bool 
    rephrase_count: int 
    question: HumanMessage 

class GradeDocument(BaseModel):
    score: str = Field(description="Os documentos são relevantes para a questão? Responda com 'Sim' se sim ou 'Não' se não")

class GradeQuestion(BaseModel):
    score: str = Field(description="A questão é adequada para o contexto? Responda com 'Sim' se sim ou 'Não' se não")


class InputDocument(BaseModel):
    file_path: str
    metadata: dict = {}
