from datetime import datetime
from typing import List, TypedDict, Union, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from io import BytesIO
from io import BufferedReader
from langchain_core.documents import Document

class InputDocument(BaseModel):
    """
    This class is used to input the document into the vector store.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    document_link: str
    document_type: Optional[str] = None
    title: str 
    group: str 
    area: str 
    number: str 
    document_date: datetime.date
    subjects: List[str]
    id: str 
    creation_date: datetime.date
    publication_date: datetime.date
    documents_processed: Optional[List[Document]] = None



class DocumentTypeResponse(BaseModel):
    document_type: str

class ResumeResponse(BaseModel):
    resume: str

class QuestionResponse(BaseModel):
    question: str
