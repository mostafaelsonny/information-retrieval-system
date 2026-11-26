"""
Unit and integration tests for IR-09: Query Vectorization & L2 Normalization Engine (Rovan).
"""
import math

import pytest

from src.indexing.positional_index import build_positional_index
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.ranking.ranking import rank_documents
from src.ranking.similarity import calculate_similarity
from src.retrieval.boolean_query import execute_boolean_query
from src.retrieval.phrase_query import search_phrase
from src.statistics.term_statistics import (
    calculate_df,
    calculate_idf,
    calculate_raw_tf,
    calculate_weighted_tf,
)
from src.vectorization.normalization import (
    calculate_document_lengths,
    normalize_tfidf,
    vectorize_query,
)
from src.vectorization.tfidf import calculate_tfidf


def test_vectorize_query_customer_service_mock():
    """Validates IR-09 using the official test snippet from the task card."""
    test_idf = {"customer": 0.15490, "service": 0.39794}
    q_norm = vectorize_query(["customer", "service"], test_idf)

    assert abs(math.sqrt(sum(v ** 2 for v in q_norm.values())) - 1.0) < 1e-6
    assert q_norm["service"] > q_norm["customer"]
    assert round(q_norm["customer"], 4) == 0.3627
    assert round(q_norm["service"], 4) == 0.9319


def test_vectorize_query_normalizes_case_and_whitespace():
    """Ensures query tokens are lowercased, stripped, and blank tokens are skipped."""
    idf = {"customer": math.log10(10 / 7), "service": math.log10(10 / 4)}

    clean_vec = vectorize_query(["customer", "service"], idf)
    messy_vec = vectorize_query([" Customer ", "SERVICE", "", "   "], idf)

    assert set(messy_vec.keys()) == {"customer", "service"}
    assert messy_vec["customer"] == pytest.approx(clean_vec["customer"], abs=1e-12)
    assert messy_vec["service"] == pytest.approx(clean_vec["service"], abs=1e-12)


def test_vectorize_query_repeated_terms_logarithmic_tf():
    """Verifies repeated query terms use WTF = 1 + log10(TF) and collection IDF."""
    idf = {"customer": math.log10(10 / 7), "service": math.log10(10 / 4)}
    q_norm = vectorize_query(["customer", "service", "customer"], idf)

    expected_c = (1.0 + math.log10(2)) * idf["customer"]
    expected_s = 1.0 * idf["service"]
    expected_len = math.sqrt(expected_c ** 2 + expected_s ** 2)

    assert q_norm["customer"] == pytest.approx(expected_c / expected_len, abs=1e-12)
    assert q_norm["service"] == pytest.approx(expected_s / expected_len, abs=1e-12)
    assert abs(math.sqrt(sum(v ** 2 for v in q_norm.values())) - 1.0) < 1e-6


def test_vectorize_query_edge_cases():
    """Covers empty query, OOV terms, and zero-IDF terms without division by zero."""
    assert vectorize_query([], {"customer": 0.1549}) == {}
    assert vectorize_query(["   ", ""], {"customer": 0.1549}) == {}

    oov_vec = vectorize_query(["unknown", "missing"], {"customer": 0.1549})
    assert oov_vec == {"unknown": 0.0, "missing": 0.0}

    zero_idf_vec = vectorize_query(["common"], {"common": 0.0})
    assert zero_idf_vec == {"common": 0.0}


def test_vectorize_query_end_to_end_ranking_ground_truth():
    """Verifies query vectorization produces exact Part B Cosine Similarity & Rankings."""
    docs = load_documents("data")
    tokenized = tokenize_documents(docs)
    pos_index = build_positional_index(tokenized, use_spark=False)

    raw_tf = calculate_raw_tf(pos_index)
    weighted_tf = calculate_weighted_tf(raw_tf)
    df = calculate_df(pos_index)
    idf = calculate_idf(df, total_documents=len(docs))
    tfidf = calculate_tfidf(weighted_tf, idf)
    doc_lengths = calculate_document_lengths(tfidf, list(docs.keys()))
    norm_tfidf = normalize_tfidf(tfidf, doc_lengths)

    # Phrase Query 1: "customer service"
    p1_res = search_phrase("customer service", pos_index)
    q1_vec = vectorize_query(["customer", "service"], idf)
    assert abs(math.sqrt(sum(v ** 2 for v in q1_vec.values())) - 1.0) < 1e-6
    sim_p1 = calculate_similarity(q1_vec, norm_tfidf, list(p1_res.keys()))
    p1_ranked = rank_documents(sim_p1)
    assert [(doc_id, round(score, 4)) for doc_id, score in p1_ranked] == [
        ("d1", 1.0000),
        ("d2", 0.6147),
        ("d5", 0.4159),
        ("d10", 0.2875),
    ]

    # Phrase Query 2: "sales growth"
    p2_res = search_phrase("sales growth", pos_index)
    q2_vec = vectorize_query(["sales", "growth"], idf)
    assert abs(math.sqrt(sum(v ** 2 for v in q2_vec.values())) - 1.0) < 1e-6
    sim_p2 = calculate_similarity(q2_vec, norm_tfidf, list(p2_res.keys()))
    p2_ranked = rank_documents(sim_p2)
    assert [(doc_id, round(score, 4)) for doc_id, score in p2_ranked] == [
        ("d5", 0.4847),
        ("d3", 0.4395),
        ("d8", 0.3240),
        ("d7", 0.3067),
    ]

    # Boolean AND: "customer service" AND "sales growth"
    and_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND")
    q_and_vec = vectorize_query(["customer", "service", "sales", "growth"], idf)
    sim_and = calculate_similarity(q_and_vec, norm_tfidf, and_res)
    and_ranked = rank_documents(sim_and)
    assert [(doc_id, round(score, 4)) for doc_id, score in and_ranked] == [("d5", 0.6376)]

    # Boolean AND NOT: "customer service" AND NOT "sales growth" (query uses Phrase 1 only)
    and_not_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND NOT")
    sim_and_not = calculate_similarity(q1_vec, norm_tfidf, and_not_res)
    and_not_ranked = rank_documents(sim_and_not)
    assert [(doc_id, round(score, 4)) for doc_id, score in and_not_ranked] == [
        ("d1", 1.0000),
        ("d2", 0.6147),
        ("d10", 0.2875),
    ]

