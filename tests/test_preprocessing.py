
import pytest

from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents


def test_load_documents_count():
    docs = load_documents("data")

    assert len(docs) == 10


def test_load_documents_content():
    docs = load_documents("data")

    assert docs["d1"] == "customer service"

    assert docs["d2"] == (
        "customer service improves customer satisfaction"
    )


def test_tokenizer_d1():
    docs = load_documents("data")
    tokens = tokenize_documents(docs)

    assert tokens["d1"] == [
        ("customer", 1),
        ("service", 2)
    ]


def test_tokenizer_d2():
    docs = load_documents("data")
    tokens = tokenize_documents(docs)

    assert tokens["d2"] == [
        ("customer", 1),
        ("service", 2),
        ("improves", 3),
        ("customer", 4),
        ("satisfaction", 5)
    ]


def test_tokenizer_lowercase_and_duplicates():
    docs = {
        "d1": "Customer CUSTOMER Service"
    }

    tokens = tokenize_documents(docs)

    assert tokens["d1"] == [
        ("customer", 1),
        ("customer", 2),
        ("service", 3)
    ]


def test_tokenizer_whitespace_only():
    docs = {
        "d1": "Customer,   Service!\tImproves"
    }

    tokens = tokenize_documents(docs)

    assert tokens["d1"] == [
        ("customer,", 1),
        ("service!", 2),
        ("improves", 3)
    ]


def test_tokenizer_preserves_stop_words():
    docs = {
        "d1": "the customer is happy"
    }

    tokens = tokenize_documents(docs)

    assert tokens["d1"] == [
        ("the", 1),
        ("customer", 2),
        ("is", 3),
        ("happy", 4)
    ]
