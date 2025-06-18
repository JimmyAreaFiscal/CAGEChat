import re, json, sys 
from pathlib import Path 
from typing import List, Dict, Any
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document
from config import Settings, settings
from modules.utils.schemas import InputDocument

ARTIGO_RE = re.compile(r"(?ms)^[\t]*Art\.?\s*\d+[º]?[--]?.*?(?=^[ \t]*Art\.|\Z)")

def load_pdf_with_langchain(path: str | Path) -> str:
    loader = PyPDFLoader(path)
    docs = loader.load() 
    pages = [doc.page_content for doc in docs]
    return "\n\n".join(pages).rstrip()


def extract_articles(text: str) -> List[str]:
    articles: List[Dict[str, Any]] = []
    matches = list(ARTIGO_RE.finditer(text))
    if matches:
        first = matches[0]
        pre_text = text[: first.start()].strip() 

        if pre_text:
            articles.append({
                "article_index": 0,
                "text": pre_text,
                "char_start": 0,
                "char_end": first.start(),
            })

    for idx, match in enumerate(matches, start=1):
        articles.append({
            "article_index": idx,
            "text": match.group().strip(),
            "char_start": match.start(),
            "char_end": match.end(),
        })

    return articles


def chunking_by_article(state: InputDocument, config: Settings = settings) -> InputDocument:
    text = load_pdf_with_langchain(state.document_link)
    articles = extract_articles(text)
    documents = []
    for article in articles:
        documents.append(Document(page_content=article['text'], metadata={
            "source": "legislation", 
            "article_index": article['article_index'],
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
