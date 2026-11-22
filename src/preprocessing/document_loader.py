"""
Member 2 (Monzer): Document Loader & Preprocessor
Reads documents from disk, converts to lowercase, strips punctuation, preserves terms.
No stop words removal, No stemming.
"""
import os
import re
from typing import Dict
from src.contracts import DocumentsContract


def clean_text(text: str) -> str:
    """Converts text to lowercase and removes punctuation while keeping single whitespace."""
    text = text.lower()
    # Replace non-alphanumeric characters with space
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Collapse multiple whitespaces
    return ' '.join(text.split())


def load_documents(data_dir: str = "data") -> DocumentsContract:
    """
    Loads all d*.txt documents from data_dir and returns a dictionary:
    {"d1": "clean content", ..., "d10": "clean content"}
    """
    documents: Dict[str, str] = {}
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")

    for i in range(1, 11):
        doc_id = f"d{i}"
        file_path = os.path.join(data_dir, f"{doc_id}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents[doc_id] = clean_text(content)
        else:
            raise FileNotFoundError(f"Expected document file '{file_path}' not found.")

    return documents
