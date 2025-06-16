"""
This module is responsible for uploading documents to the vector store.

This is based on each document type, where the allowed

"""

from docling.document_converter import DocumentConverter
from typing import List
from langchain.schema import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
import logging

logging.basicConfig(level=logging.INFO)

ALLOWED_DOCUMENT_TYPES = ['manual', 'guia', 'livro', 'lei', 'instrução normativa', 'norma', 'jurisprudência', 'parecer']


class CustomLoader:
    """
    This class is responsible for loading documents from a file path, based on the document type.
    This can be extended to other document types, as long as they are supported by the DocumentConverter.
    """
    def __init__(self, file_path: str, metadata: dict):
        assert isinstance(metadata, dict), "Metadados informados de forma inválida"
        assert 'tipo_documento' in metadata.keys(), "Tipo de documento não informado"
        assert metadata.get('tipo_documento') in ALLOWED_DOCUMENT_TYPES, "Tipo de documento inválido"
        self.file_path = file_path
        self.metadata = metadata
        self.headers_to_split_on = []
        
        if metadata.get('tipo_documento') in ['manual', 'guia', 'livro']:
            self.headers_to_split_on = [
                ("#", "Capítulo"),
                ("##", "Subcapítulo"),
                ("###", "Subsubcapítulo")
            ]
        elif metadata.get('tipo_documento') in ['lei', 'instrução normativa', 'norma']:
            self.headers_to_split_on = [
                ("art.", "artigo"),
                ("§", "parágrafo")
                
            ]
        elif metadata.get('tipo_documento') in ['jurisprudência', 'parecer']:
            self.headers_to_split_on = [
                ("EMENTA", "ementa"),
                ("ACÓRDÃO", "acórdão"),
                ("VOTO", "voto")
            ]
        else:
            # Default splitting for other document types
            self.headers_to_split_on = [
                ("#", "capítulo"),
                ("##", "subcapítulo"),
                ("###", "subsubcapítulo")
            ]

    def load(self) -> List[Document]:
        logging.info(f"Start loading the document: {self.file_path.split('.')[-2]}")
        converter = DocumentConverter()
        markdown_document = converter.convert(self.file_path).document.export_to_markdown()
        markdown_splitter = MarkdownHeaderTextSplitter(self.headers_to_split_on)
        docs_list = markdown_splitter.split_text(markdown_document)
        for doc in docs_list:
            doc.metadata.update(self.metadata)
        return docs_list
    




