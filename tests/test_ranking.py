"""
Unit and integration tests for IR-12: Cosine Similarity & Ranking Engine (Febronia).
"""
import math

import pytest

from src.contracts import validate_similarity
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


def test_calculate_similarity_mock_dot_product():
    """Validates Dot Product cosine similarity on normalized mock vectors."""
    q_norm = {"customer": 0.3627, "service": 0.9319}
    norm_tfidf = {
        "customer": {"d1": 0.3627, "d2": 0.2},
        "service": {"d1": 0.9319, "d2": 0.5},
        "unrelated": {"d3": 1.0},
    }

    scores = calculate_similarity(q_norm, norm_tfidf, ["d1", "d2"])

    assert set(scores.keys()) == {"d1", "d2"}
    assert "d3" not in scores
    assert scores["d1"] == pytest.approx(0.3627**2 + 0.9319**2, abs=1e-9)
    assert scores["d2"] == pytest.approx(0.3627 * 0.2 + 0.9319 * 0.5, abs=1e-9)
    assert validate_similarity({"customer service": scores}) is True


def test_calculate_similarity_edge_cases():
    """Covers empty target_docs, empty query vector, and OOV terms."""
    norm_tfidf = {"customer": {"d1": 1.0}}

    assert calculate_similarity({"customer": 1.0}, norm_tfidf, []) == {}
    assert calculate_similarity({}, norm_tfidf, ["d1", "d2"]) == {"d1": 0.0, "d2": 0.0}
    assert calculate_similarity({"unknown": 1.0}, norm_tfidf, ["d1"]) == {"d1": 0.0}


def test_rank_documents_descending_and_natural_tie_breaking():
    """Verifies descending score order and natural ascending doc_id tie-breaking."""
    scores = {
        "d10": 0.5,
        "d2": 0.5,
        "d1": 0.5,
        "d5": 0.9,
        "d3": 0.2,
    }
    ranked = rank_documents(scores)
    assert ranked == [
        ("d5", 0.9),
        ("d1", 0.5),
        ("d2", 0.5),
        ("d10", 0.5),
        ("d3", 0.2),
    ]


def test_rank_documents_empty_and_non_standard_ids():
    """Covers empty score dict and non-d<int> document IDs during tie-breaking."""
    assert rank_documents({}) == []
    assert rank_documents({"doc_b": 0.5, "d10": 0.5, "d2": 0.5, "doc_a": 0.5}) == [
        ("d2", 0.5),
        ("d10", 0.5),
        ("doc_a", 0.5),
        ("doc_b", 0.5),
    ]


def test_ground_truth_similarity_and_ranking_all_four_queries():
    """Validates exact scores, [0, 1] bounds, and rankings for all 4 official Business queries."""
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

    # 1. Phrase Query: "customer service" -> d1 > d2 > d5 > d10 (d1 == 1.0)
    p1_res = search_phrase("customer service", pos_index)
    q1_vec = vectorize_query(["customer", "service"], idf)
    sim_p1 = calculate_similarity(q1_vec, norm_tfidf, list(p1_res.keys()))
    p1_ranked = rank_documents(sim_p1)
    assert [doc_id for doc_id, _ in p1_ranked] == ["d1", "d2", "d5", "d10"]
    assert p1_ranked[0][1] == pytest.approx(1.0, abs=1e-6)
    assert [(doc_id, round(score, 4)) for doc_id, score in p1_ranked] == [
        ("d1", 1.0000),
        ("d2", 0.6147),
        ("d5", 0.4159),
        ("d10", 0.2875),
    ]

    # 2. Phrase Query: "sales growth" -> d5 > d3 > d8 > d7
    p2_res = search_phrase("sales growth", pos_index)
    q2_vec = vectorize_query(["sales", "growth"], idf)
    sim_p2 = calculate_similarity(q2_vec, norm_tfidf, list(p2_res.keys()))
    p2_ranked = rank_documents(sim_p2)
    assert [doc_id for doc_id, _ in p2_ranked] == ["d5", "d3", "d8", "d7"]
    assert [(doc_id, round(score, 4)) for doc_id, score in p2_ranked] == [
        ("d5", 0.4847),
        ("d3", 0.4395),
        ("d8", 0.3240),
        ("d7", 0.3067),
    ]

    # 3. Boolean AND: "customer service" AND "sales growth" -> d5 only
    and_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND")
    q_and_vec = vectorize_query(["customer", "service", "sales", "growth"], idf)
    sim_and = calculate_similarity(q_and_vec, norm_tfidf, and_res)
    and_ranked = rank_documents(sim_and)
    assert [(doc_id, round(score, 4)) for doc_id, score in and_ranked] == [("d5", 0.6376)]

    # 4. Boolean AND NOT: "customer service" AND NOT "sales growth" -> d1 > d2 > d10
    # Query vector built exclusively from Phrase 1 ("customer service")
    and_not_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND NOT")
    sim_and_not = calculate_similarity(q1_vec, norm_tfidf, and_not_res)
    and_not_ranked = rank_documents(sim_and_not)
    assert [doc_id for doc_id, _ in and_not_ranked] == ["d1", "d2", "d10"]
    assert [(doc_id, round(score, 4)) for doc_id, score in and_not_ranked] == [
        ("d1", 1.0000),
        ("d2", 0.6147),
        ("d10", 0.2875),
    ]

    assert validate_similarity(
        {
            "customer service": sim_p1,
            "sales growth": sim_p2,
            "customer service AND sales growth": sim_and,
            "customer service AND NOT sales growth": sim_and_not,
        }
    ) is True
