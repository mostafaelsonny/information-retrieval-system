"""
Unit and integration tests for IR-08: Document Vector L2 Norms & Matrix Normalization Engine (Rovan).
"""
import math

import pytest

from src.contracts import validate_tfidf_and_norms
from src.indexing.positional_index import build_positional_index
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.statistics.term_statistics import (
    calculate_df,
    calculate_idf,
    calculate_raw_tf,
    calculate_weighted_tf,
)
from src.vectorization.normalization import (
    calculate_document_lengths,
    normalize_tfidf,
)
from src.vectorization.tfidf import calculate_tfidf


def test_calculate_document_lengths_and_unit_vectors_mock():
    """Validates L2 Euclidean length and unit-vector property using a 3-4-5 triangle mock."""
    mock_tfidf = {
        "customer": {"d1": 3.0, "d2": 0.0},
        "service": {"d1": 4.0, "d2": 5.0},
    }
    doc_ids = ["d1", "d2"]

    doc_lengths = calculate_document_lengths(mock_tfidf, doc_ids)
    assert doc_lengths["d1"] == pytest.approx(5.0, abs=1e-12)
    assert doc_lengths["d2"] == pytest.approx(5.0, abs=1e-12)

    normalized = normalize_tfidf(mock_tfidf, doc_lengths)
    assert normalized["customer"]["d1"] == pytest.approx(0.6, abs=1e-12)
    assert normalized["service"]["d1"] == pytest.approx(0.8, abs=1e-12)
    assert normalized["customer"]["d2"] == pytest.approx(0.0, abs=1e-12)
    assert normalized["service"]["d2"] == pytest.approx(1.0, abs=1e-12)

    # Golden check from IR-08: every non-zero normalized document vector has L2 norm == 1.0
    for d in doc_ids:
        sum_sq = sum(normalized[term][d] ** 2 for term in normalized)
        assert abs(math.sqrt(sum_sq) - 1.0) < 1e-6, f"Doc {d} is not normalized properly!"


def test_normalize_tfidf_complete_matrix_with_sparse_input():
    """Ensures sparse TF-IDF inputs produce a complete matrix with 0.0 for absent terms."""
    sparse_tfidf = {
        "customer": {"d1": 3.0},
        "service": {"d1": 4.0, "d2": 2.0},
    }
    doc_ids = ["d1", "d2", "d3"]

    doc_lengths = calculate_document_lengths(sparse_tfidf, doc_ids)
    assert doc_lengths["d1"] == pytest.approx(5.0, abs=1e-12)
    assert doc_lengths["d2"] == pytest.approx(2.0, abs=1e-12)
    assert doc_lengths["d3"] == 0.0

    normalized = normalize_tfidf(sparse_tfidf, doc_lengths)

    # All doc_ids exist as keys for every term (no KeyError on direct indexing)
    for term in normalized:
        assert set(normalized[term].keys()) == {"d1", "d2", "d3"}

    assert normalized["customer"]["d2"] == 0.0
    assert normalized["customer"]["d3"] == 0.0
    assert normalized["service"]["d3"] == 0.0

    for d in ["d1", "d2"]:
        sum_sq = sum(normalized[term][d] ** 2 for term in normalized)
        assert abs(math.sqrt(sum_sq) - 1.0) < 1e-6


def test_normalization_edge_cases():
    """Covers empty inputs, zero-length documents (safe division), and missing doc_lengths."""
    assert calculate_document_lengths({}, []) == {}
    assert calculate_document_lengths({}, ["d1", "d2"]) == {"d1": 0.0, "d2": 0.0}
    assert normalize_tfidf({}, {"d1": 1.0}) == {}

    zero_tfidf = {"common": {"d1": 0.0}}
    lengths = calculate_document_lengths(zero_tfidf, ["d1"])
    assert lengths["d1"] == 0.0

    normalized = normalize_tfidf(zero_tfidf, lengths)
    assert normalized["common"]["d1"] == 0.0

    # Document missing from document_lengths defaults safely to 0.0
    partial_norm = normalize_tfidf({"term": {"d99": 1.5}}, {})
    assert partial_norm["term"]["d99"] == 0.0


def test_normalization_pipeline_integration_all_ten_docs():
    """End-to-end verification across all 10 business documents matching Part A ground truth."""
    docs = load_documents("data")
    doc_ids = sorted(docs.keys(), key=lambda x: int(x[1:]))
    tokenized = tokenize_documents(docs)
    pos_index = build_positional_index(tokenized, use_spark=False)

    raw_tf = calculate_raw_tf(pos_index)
    weighted_tf = calculate_weighted_tf(raw_tf)
    df = calculate_df(pos_index)
    idf = calculate_idf(df, total_documents=len(docs))
    tfidf = calculate_tfidf(weighted_tf, idf)

    doc_lengths = calculate_document_lengths(tfidf, doc_ids)
    assert set(doc_lengths.keys()) == {f"d{i}" for i in range(1, 11)}
    assert all(doc_lengths[d] > 0.0 for d in doc_ids)

    normalized = normalize_tfidf(tfidf, doc_lengths)

    # Verify d1 normalized weights match results/part_a_tables.txt
    assert round(normalized["customer"]["d1"], 4) == 0.3627
    assert round(normalized["service"]["d1"], 4) == 0.9319

    # Golden property: all 10 documents have L2 norm == 1.0000 (+- 1e-6)
    for d in doc_ids:
        sum_sq = sum(normalized[term][d] ** 2 for term in normalized)
        assert abs(math.sqrt(sum_sq) - 1.0) < 1e-6, f"Doc {d} is not normalized properly!"

    assert validate_tfidf_and_norms(tfidf, doc_lengths, normalized) is True

