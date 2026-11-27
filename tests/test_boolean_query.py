"""
Unit and integration tests for IR-11: Boolean Retrieval Engine (Febronia).
"""
import pytest

from src.indexing.positional_index import build_positional_index
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.retrieval.boolean_query import execute_boolean_query
from src.retrieval.phrase_query import search_phrase


MOCK_CUSTOMER_SERVICE_DOCS = ["d1", "d2", "d5", "d10"]
MOCK_SALES_GROWTH_DOCS = ["d3", "d5", "d7", "d8"]


def test_boolean_and_ground_truth_mock():
    """Validates Boolean AND (set intersection) on Business mock phrase results."""
    result = execute_boolean_query(
        MOCK_CUSTOMER_SERVICE_DOCS,
        MOCK_SALES_GROWTH_DOCS,
        "AND",
    )
    assert result == ["d5"]


def test_boolean_and_not_ground_truth_mock():
    """Validates Boolean AND NOT (set difference) on Business mock phrase results."""
    result = execute_boolean_query(
        MOCK_CUSTOMER_SERVICE_DOCS,
        MOCK_SALES_GROWTH_DOCS,
        "AND NOT",
    )
    assert result == ["d1", "d2", "d10"]


def test_natural_numeric_sorting():
    """Ensures d10 is ordered after d2 and d9 rather than lexicographically after d1."""
    result = execute_boolean_query(
        ["d10", "d2", "d1", "d9"],
        [],
        "AND NOT",
    )
    assert result == ["d1", "d2", "d9", "d10"]


def test_operator_normalization_and_not_alias():
    """Validates case-insensitivity, whitespace normalization, and NOT alias."""
    assert execute_boolean_query(MOCK_CUSTOMER_SERVICE_DOCS, MOCK_SALES_GROWTH_DOCS, "  and ") == ["d5"]
    assert execute_boolean_query(MOCK_CUSTOMER_SERVICE_DOCS, MOCK_SALES_GROWTH_DOCS, " and   not ") == [
        "d1",
        "d2",
        "d10",
    ]
    assert execute_boolean_query(MOCK_CUSTOMER_SERVICE_DOCS, MOCK_SALES_GROWTH_DOCS, "not") == [
        "d1",
        "d2",
        "d10",
    ]


def test_empty_input_edge_cases():
    """Covers cases where one or both input document lists are empty."""
    assert execute_boolean_query([], MOCK_SALES_GROWTH_DOCS, "AND") == []
    assert execute_boolean_query(MOCK_CUSTOMER_SERVICE_DOCS, [], "AND") == []
    assert execute_boolean_query([], MOCK_SALES_GROWTH_DOCS, "AND NOT") == []
    assert execute_boolean_query(MOCK_CUSTOMER_SERVICE_DOCS, [], "AND NOT") == [
        "d1",
        "d2",
        "d5",
        "d10",
    ]
    assert execute_boolean_query([], [], "AND") == []
    assert execute_boolean_query([], [], "AND NOT") == []


def test_disjoint_and_duplicate_inputs():
    """Covers disjoint sets, duplicate IDs, and fallback sorting for non-standard IDs."""
    assert execute_boolean_query(["d1", "d1", "d2"], ["d3", "d4"], "AND") == []
    assert execute_boolean_query(["d2", "d1", "d2"], ["d3"], "AND NOT") == ["d1", "d2"]
    assert execute_boolean_query(["doc_b", "d10", "d2", "doc_a"], [], "AND NOT") == [
        "d2",
        "d10",
        "doc_a",
        "doc_b",
    ]


@pytest.mark.parametrize("bad_op", ["OR", "XOR", "", "   ", "NAND"])
def test_unsupported_operator_raises_value_error(bad_op):
    """Ensures unsupported Boolean operators raise ValueError."""
    with pytest.raises(ValueError, match="Unsupported Boolean operator"):
        execute_boolean_query(MOCK_CUSTOMER_SERVICE_DOCS, MOCK_SALES_GROWTH_DOCS, bad_op)


def test_boolean_query_dataset_integration():
    """Validates Phrase -> Boolean pipeline on the Business dataset against Ground Truth."""
    docs = load_documents("data")
    tokenized = tokenize_documents(docs)
    pos_index = build_positional_index(tokenized, use_spark=False)

    p1_docs = list(search_phrase("customer service", pos_index).keys())
    p2_docs = list(search_phrase("sales growth", pos_index).keys())

    assert execute_boolean_query(p1_docs, p2_docs, "AND") == ["d5"]
    assert execute_boolean_query(p1_docs, p2_docs, "AND NOT") == ["d1", "d2", "d10"]
