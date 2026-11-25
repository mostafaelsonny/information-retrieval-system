
import os
from src.contracts import DocumentsContract


def load_documents(data_path: str = "data") -> DocumentsContract:
    """
    Reads documents d1.txt to d10.txt
    and returns their content in a dictionary.
    """

    documents: DocumentsContract = {}

    for i in range(1, 11):
        doc_id = f"d{i}"
        file_path = os.path.join(data_path, f"{doc_id}.txt")

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Missing required document: {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            raise ValueError(f"Document {doc_id} is empty!")

        documents[doc_id] = content

    return documents
