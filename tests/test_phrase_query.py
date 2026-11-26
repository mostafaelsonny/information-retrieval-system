"""
Unit and integration tests for IR-10: Positional Phrase Query Engine (Febronia).
"""
import pytest

from src.indexing.positional_index import build_positional_index
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.retrieval.phrase_query import search_phrase


MOCK_POSITIONAL_INDEX = {
    "accelerates": {"d5": [3]},
    "customer": {
        "d1": [1],
        "d2": [1, 4],
        "d4": [4],
        "d5": [1, 6],
        "d7": [7],
        "d9": [6],
        "d10": [1, 4],
    },
    "growth": {
        "d3": [2],
        "d5": [5],
        "d7": [5],
        "d8": [2],
    },
    "sales": {
        "d3": [1],
        "d5": [4, 9],
        "d7": [4],
        "d8": [1, 3],
    },
    "service": {
        "d1": [2],
        "d2": [2],
        "d5": [2, 7],
        "d10": [2],
    },
}


def test_customer_service_phrase_mock():
    """Validates exact starting positions for 'customer service' on mock index."""
    result = search_phrase("customer service", MOCK_POSITIONAL_INDEX)
    assert result == {
        "d1": [1],
        "d2": [1],
        "d5": [1, 6],
        "d10": [1],
    }
    assert list(result.keys()) == ["d1", "d2", "d5", "d10"]


def test_sales_growth_phrase_mock():
    """Validates exact starting positions for 'sales growth' on mock index."""
    result = search_phrase("sales growth", MOCK_POSITIONAL_INDEX)
    assert result == {
        "d3": [1],
        "d5": [4],
        "d7": [4],
        "d8": [1],
    }
    assert list(result.keys()) == ["d3", "d5", "d7", "d8"]


def test_multi_word_phrase():
    """Validates 3+ consecutive term matching (pos + 1, pos + 2, ...)."""
    result = search_phrase("customer service accelerates sales growth", MOCK_POSITIONAL_INDEX)
    assert result == {"d5": [1]}


def test_single_word_query_returns_positions_copy():
    """Validates single-word query returns naturally sorted docs and copied position lists."""
    result = search_phrase("growth", MOCK_POSITIONAL_INDEX)
    assert result == {
        "d3": [2],
        "d5": [5],
        "d7": [5],
        "d8": [2],
    }
    result["d3"].append(999)
    assert MOCK_POSITIONAL_INDEX["growth"]["d3"] == [2]


def test_edge_cases():
    """Covers empty queries, whitespace/casing normalization, reversed order, and unknown terms."""
    assert search_phrase("", MOCK_POSITIONAL_INDEX) == {}
    assert search_phrase("   ", MOCK_POSITIONAL_INDEX) == {}
    assert search_phrase("  Customer   Service  ", MOCK_POSITIONAL_INDEX) == {
        "d1": [1],
        "d2": [1],
        "d5": [1, 6],
        "d10": [1],
    }
    # Reversed order: terms exist in d1, d2, d5, d10 but not in order "service customer"
    assert search_phrase("service customer", MOCK_POSITIONAL_INDEX) == {}
    # Unknown term
    assert search_phrase("unknown phrase", MOCK_POSITIONAL_INDEX) == {}
    # Empty index
    assert search_phrase("customer service", {}) == {}


def test_non_adjacent_terms_do_not_match():
    """Ensures terms appearing in the same document at non-consecutive positions do not match."""
    index = {
        "customer": {"d1": [1, 5]},
        "service": {"d1": [3, 8]},
    }
    assert search_phrase("customer service", index) == {}


def test_phrase_query_dataset_integration():
    """Validates Ground Truth starting positions on the real Business dataset."""
    docs = load_documents("data")
    tokenized = tokenize_documents(docs)
    pos_index = build_positional_index(tokenized, use_spark=False)

    assert search_phrase("customer service", pos_index) == {
        "d1": [1],
        "d2": [1],
        "d5": [1, 6],
        "d10": [1],
    }
    assert search_phrase("sales growth", pos_index) == {
        "d3": [1],
        "d5": [4],
        "d7": [4],
        "d8": [1],
    }
