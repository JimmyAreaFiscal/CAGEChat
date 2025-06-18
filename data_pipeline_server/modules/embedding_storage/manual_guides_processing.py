import re, json, sys 
from pathlib import Path 
from typing import List, Dict, Any
from langchain_text_splitters.markdown import MarkdownHeaderTextSplitter
from docling.document_converter import DocumentConverter
from data_pipeline_server.modules.utils.schemas import InputDocument

ARTIGO_RE = re.compile(r"(?ms)^[\t]*Art\.?\s*\d+[º]?[--]?.*?(?=^[ \t]*Art\.|\Z)")


def load_with_docling(path: str | Path) -> str:
    source = "https://sincage.sefaz.rs.gov.br/api/arquivo/Manual%20de%20orientacao%20do%20gestor%20publico%205a%20ed%202022%20semlogo_83273.pdf"  # document per local path or URL
    converter = DocumentConverter()
    doc = converter.convert(source).document
    return doc.export_to_markdown()


def extract_chapters(text: str) -> List[str]:
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "Documento"),("##", "Capítulo"), ("###", "Subcapítulo")])
    return splitter.split_text(text)


def chunking_by_chapter(state: InputDocument) -> InputDocument:
    text = load_with_docling(state.document_link)
    chapters = extract_chapters(text)
    documents = []
    for chapter in chapters:
        documents.append(Document(page_content=chapter, metadata={
            "source": "manual_guide", 
            "chapter_index": chapter['chapter_index'],
            "title": state.title,
            "group": state.group,
            "area": state.area,
            "number": state.number,
            "document_date": state.document_date,
            "subjects": state.subjects,
            "id": state.id,
            "creation_date": state.creation_date,
            "publication_date": state.publication_date
        }))
    state.documents_processed = documents
    return state
