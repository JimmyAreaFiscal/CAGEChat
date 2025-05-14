from typing import TypedDict, List, Dict, Annotated, Literal, Any
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.documents import Document

State = None


class AgentState(TypedDict):
    
    messages: List[BaseMessage]
    question: HumanMessage 
    subquestions: List[str]

    qa_context: List[Dict[Literal['question', 'answer', 'document'], Any]]

    agent_think: str
    on_topic: str 
    rephrased_question: str 
    proceed_to_generate: bool 


    
    
    


class RetrievalState(TypedDict):
    """
    This is a state for the retrieval subgraph.
    It is used to store the documents, the agent think and the score.
    """
    original_question: HumanMessage
    retrieval_question: HumanMessage
    answer: Annotated[dict, None] = Field(description="Dicionário com a pergunta, resposta e o contexto")
    documents: List[Document]
    agent_think: str
    proceed_to_generate: bool
    rephrase_count: int



class GradeDocument(BaseModel):
    score: str = Field(description="Os documentos são relevantes para a questão? Responda com 'Sim' se sim ou 'Não' se não")

class GradeQuestion(BaseModel):
    score: str = Field(description="A questão é adequada para o contexto? Responda com 'Sim' se sim ou 'Não' se não")


class InputDocument(BaseModel):
    file_path: str
    metadata: dict = {}

class DecomposedQuestion(BaseModel):
    subquestions: List[str] = Field(description="Lista com as subquestões independentes.")