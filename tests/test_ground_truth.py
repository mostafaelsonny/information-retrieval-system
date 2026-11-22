"""
Validates Ground Truth matches for the Business Dataset.
Queries tested:
1. "customer service" -> ['d1', 'd2', 'd5', 'd10']
2. "sales growth" -> ['d3', 'd5', 'd7', 'd8']
3. "customer service" AND "sales growth" -> ['d5']
4. "customer service" AND NOT "sales growth" -> ['d1', 'd2', 'd10']
"""
import pytest
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.indexing.positional_index import build_positional_index
from src.retrieval.phrase_query import search_phrase
from src.retrieval.boolean_query import execute_boolean_query


@pytest.fixture(scope="module")
def positional_index():
    docs = load_documents("data")
    tokens = tokenize_documents(docs)
    return build_positional_index(tokens)


def test_phrase_query_1(positional_index):
    res = search_phrase("customer service", positional_index)
    matching_docs = sorted(list(res.keys()), key=lambda x: int(x[1:]))
    assert matching_docs == ["d1", "d2", "d5", "d10"], f"Expected ['d1', 'd2', 'd5', 'd10'], got {matching_docs}"


def test_phrase_query_2(positional_index):
    res = search_phrase("sales growth", positional_index)
    matching_docs = sorted(list(res.keys()), key=lambda x: int(x[1:]))
    assert matching_docs == ["d3", "d5", "d7", "d8"], f"Expected ['d3', 'd5', 'd7', 'd8'], got {matching_docs}"


def test_boolean_and(positional_index):
    p1_res = search_phrase("customer service", positional_index)
    p2_res = search_phrase("sales growth", positional_index)
    and_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND")
    assert and_res == ["d5"], f"Expected ['d5'], got {and_res}"


def test_boolean_and_not(positional_index):
    p1_res = search_phrase("customer service", positional_index)
    p2_res = search_phrase("sales growth", positional_index)
    and_not_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND NOT")
    assert and_not_res == ["d1", "d2", "d10"], f"Expected ['d1', 'd2', 'd10'], got {and_not_res}"
