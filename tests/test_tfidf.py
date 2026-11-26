"""
Unit and integration tests for IR-07: TF-IDF Matrix Construction Engine (Rovan).
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


def test_calculate_tfidf_mock_data():
    """Validates IR-07 using the official mock statistics from the task card."""
    mock_wtf = {"customer": {"d1": 1.0, "d2": 1.30103}}
    mock_idf = {"customer": 0.15490}

    matrix = calculate_tfidf(mock_wtf, mock_idf)

    assert round(matrix["customer"]["d1"], 4) == 0.1549
    assert round(matrix["customer"]["d2"], 4) == 0.2015
    assert isinstance(matrix["customer"]["d1"], float)
    assert isinstance(matrix["customer"]["d2"], float)


def test_calculate_tfidf_preserves_full_precision():
    """Ensures no intermediate rounding is applied during TF-IDF multiplication."""
    exact_wtf_d2 = 1.0 + math.log10(2)
    exact_idf_customer = math.log10(10 / 7)

    weighted_tf = {"customer": {"d1": 1.0, "d2": exact_wtf_d2}}
    idf = {"customer": exact_idf_customer}

    matrix = calculate_tfidf(weighted_tf, idf)

    assert matrix["customer"]["d1"] == pytest.approx(exact_idf_customer, rel=1e-12, abs=1e-12)
    assert matrix["customer"]["d2"] == pytest.approx(
        exact_wtf_d2 * exact_idf_customer,
        rel=1e-12,
        abs=1e-12,
    )


def test_calculate_tfidf_multiple_terms_and_docs():
    """Validates TF-IDF across multiple terms and documents."""
    weighted_tf = {
        "customer": {"d1": 1.0, "d2": 1.0 + math.log10(2)},
        "service": {"d1": 1.0, "d2": 1.0},
        "revenue": {"d3": 1.0},
    }
    idf = {
        "customer": math.log10(10 / 7),
        "service": math.log10(10 / 4),
        "revenue": math.log10(10 / 1),
    }

    matrix = calculate_tfidf(weighted_tf, idf)

    assert set(matrix.keys()) == {"customer", "service", "revenue"}
    assert set(matrix["customer"].keys()) == {"d1", "d2"}
    assert matrix["service"]["d1"] == pytest.approx(math.log10(10 / 4), rel=1e-12)
    assert matrix["revenue"]["d3"] == pytest.approx(1.0, rel=1e-12)


def test_calculate_tfidf_edge_cases():
    """Covers empty inputs, missing IDF terms, zero WTF, and zero IDF (DF == N)."""
    assert calculate_tfidf({}, {}) == {}

    weighted_tf = {
        "unknown_term": {"d1": 1.0},
        "zero_wtf_term": {"d1": 0.0},
        "common_term": {"d1": 1.0, "d2": 1.30103},
    }
    idf = {
        "zero_wtf_term": 0.5,
        "common_term": math.log10(10 / 10),  # 0.0
    }

    matrix = calculate_tfidf(weighted_tf, idf)

    assert matrix["unknown_term"]["d1"] == 0.0
    assert matrix["zero_wtf_term"]["d1"] == 0.0
    assert matrix["common_term"]["d1"] == 0.0
    assert matrix["common_term"]["d2"] == 0.0


def test_calculate_tfidf_pipeline_integration():
    """Verifies integration from document loading/indexing/statistics through normalization."""
    docs = load_documents("data")
    tokenized = tokenize_documents(docs)
    pos_index = build_positional_index(tokenized, use_spark=False)

    raw_tf = calculate_raw_tf(pos_index)
    weighted_tf = calculate_weighted_tf(raw_tf)
    df = calculate_df(pos_index)
    idf = calculate_idf(df, total_documents=len(docs))

    tfidf = calculate_tfidf(weighted_tf, idf)

    assert len(tfidf) == len(pos_index)
    assert round(tfidf["customer"]["d1"], 4) == 0.1549
    assert round(tfidf["customer"]["d2"], 4) == 0.2015

    doc_lengths = calculate_document_lengths(tfidf, list(docs.keys()))
    norm_tfidf = normalize_tfidf(tfidf, doc_lengths)
    assert validate_tfidf_and_norms(tfidf, doc_lengths, norm_tfidf) is True

