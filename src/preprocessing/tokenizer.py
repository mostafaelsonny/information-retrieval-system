
from src.contracts import DocumentsContract, TokenizedDocumentsContract


def tokenize_documents(
    documents: DocumentsContract
) -> TokenizedDocumentsContract:
    """
    Converts each document into (term, position) tuples.
    Positions start from 1.
    """

    tokenized: TokenizedDocumentsContract = {}

    for doc_id, text in documents.items():
        words = text.lower().split()

        tokenized[doc_id] = [
            (word, pos)
            for pos, word in enumerate(words, start=1)
        ]

    return tokenized
