"""
Member 2 (Monzer): Document Tokenizer
Extracts terms and assigns 1-based sequential positions within each document.
"""
from typing import Dict, List, Tuple
from src.contracts import DocumentsContract, TokenizedDocumentsContract


def tokenize_documents(documents: DocumentsContract) -> TokenizedDocumentsContract:
    """
    Tokenizes each document into a list of (term, 1-based position) tuples.
    Example:
    "d1": [("customer", 1), ("service", 2)]
    """
    tokenized: TokenizedDocumentsContract = {}
    for doc_id, text in documents.items():
        tokens = text.split()
        # 1-based indexing as mandated by the Project Spec
        tokenized[doc_id] = [(term, pos) for pos, term in enumerate(tokens, start=1)]
    return tokenized
