
import pytest

from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.indexing.positional_index import build_positional_index


@pytest.fixture(scope="module")
def tokenized_documents():
    documents = load_documents("data")
    return tokenize_documents(documents)


@pytest.fixture(scope="module")
def python_index(tokenized_documents):
    return build_positional_index(tokenized_documents)


def test_index_is_not_empty(python_index):
    assert python_index


def test_customer_positions(python_index):
    assert python_index["customer"] == {
        "d1": [1],
        "d2": [1, 4],
        "d4": [4],
        "d5": [1, 6],
        "d7": [7],
        "d9": [6],
        "d10": [1, 4],
    }


def test_service_positions(python_index):
    assert python_index["service"] == {
        "d1": [2],
        "d2": [2],
        "d5": [2, 7],
        "d10": [2],
    }


def test_sales_positions(python_index):
    assert python_index["sales"] == {
        "d3": [1],
        "d5": [4, 9],
        "d7": [4],
        "d8": [1, 3],
    }


def test_growth_positions(python_index):
    assert python_index["growth"] == {
        "d3": [2],
        "d5": [5],
        "d7": [5],
        "d8": [2],
    }


def test_positions_are_sorted(python_index):
    for postings in python_index.values():
        for positions in postings.values():
            assert positions == sorted(positions)


def test_terms_are_sorted(python_index):
    terms = list(python_index.keys())
    assert terms == sorted(terms)


def test_document_ids_are_sorted(python_index):
    for postings in python_index.values():
        doc_ids = list(postings.keys())
        expected = sorted(doc_ids, key=lambda doc_id: int(doc_id[1:]))
        assert doc_ids == expected


def test_repeated_terms_preserve_positions():
    tokenized_docs = {
        "d1": [
            ("customer", 1),
            ("service", 2),
            ("customer", 3),
            ("customer", 4),
        ]
    }

    index = build_positional_index(tokenized_docs)

    assert index == {
        "customer": {"d1": [1, 3, 4]},
        "service": {"d1": [2]},
    }


def test_spark_matches_python(tokenized_documents, python_index):
    spark_index = build_positional_index(
        tokenized_documents,
        use_spark=True,
    )

    assert spark_index == python_index
