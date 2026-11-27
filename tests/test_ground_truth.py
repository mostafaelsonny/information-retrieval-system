"""
Comprehensive End-to-End Ground Truth Validation Suite (IR-14).
Validates 100% of Part A & Part B requirements against benchmark figures.
"""
import pytest
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.indexing.positional_index import build_positional_index
from src.statistics.term_statistics import (
    calculate_raw_tf,
    calculate_weighted_tf,
    calculate_df,
    calculate_idf,
)
from src.vectorization.tfidf import calculate_tfidf
from src.vectorization.normalization import (
    calculate_document_lengths,
    normalize_tfidf,
    vectorize_query,
)
from src.retrieval.phrase_query import search_phrase
from src.retrieval.boolean_query import execute_boolean_query
from src.ranking.similarity import calculate_similarity
from src.ranking.ranking import rank_documents


@pytest.fixture(scope="module")
def pipeline_data():
    docs = load_documents("data")
    tokens = tokenize_documents(docs)
    pos_index = build_positional_index(tokens)
    raw_tf = calculate_raw_tf(pos_index)
    weighted_tf = calculate_weighted_tf(raw_tf)
    df = calculate_df(pos_index)
    idf = calculate_idf(df, total_documents=len(docs))
    tfidf = calculate_tfidf(weighted_tf, idf)
    doc_lengths = calculate_document_lengths(tfidf, list(docs.keys()))
    norm_tfidf = normalize_tfidf(tfidf, doc_lengths)
    return {
        "docs": docs,
        "tokens": tokens,
        "pos_index": pos_index,
        "raw_tf": raw_tf,
        "weighted_tf": weighted_tf,
        "df": df,
        "idf": idf,
        "tfidf": tfidf,
        "doc_lengths": doc_lengths,
        "norm_tfidf": norm_tfidf,
    }


def test_part_a_corpus_dimensions(pipeline_data):
    """Verifies N=10 and vocabulary size V=25."""
    assert len(pipeline_data["docs"]) == 10
    assert len(pipeline_data["pos_index"]) == 25
    assert len(pipeline_data["df"]) == 25
    assert len(pipeline_data["idf"]) == 25


def test_part_a_l2_unit_lengths(pipeline_data):
    """Verifies that all normalized document vectors have L2 norm equal to 1.0."""
    norm_tfidf = pipeline_data["norm_tfidf"]
    doc_ids = list(pipeline_data["docs"].keys())
    for doc_id in doc_ids:
        squared_sum = sum(
            norm_tfidf[term].get(doc_id, 0.0) ** 2
            for term in pipeline_data["pos_index"].keys()
        )
        assert squared_sum == pytest.approx(1.0, abs=1e-5), f"L2 norm failed for {doc_id}"


def test_part_b_phrase_query_1_ground_truth(pipeline_data):
    """Phrase 1: 'customer service' -> d1, d2, d5, d10 with exact ranking and similarity."""
    pos_index = pipeline_data["pos_index"]
    norm_tfidf = pipeline_data["norm_tfidf"]
    idf = pipeline_data["idf"]

    res = search_phrase("customer service", pos_index)
    assert sorted(list(res.keys()), key=lambda x: int(x[1:])) == ["d1", "d2", "d5", "d10"]
    assert res["d1"] == [1]
    assert res["d2"] == [1]
    assert res["d5"] == [1, 6]
    assert res["d10"] == [1]

    q_vec = vectorize_query(["customer", "service"], idf)
    sim = calculate_similarity(q_vec, norm_tfidf, list(res.keys()))
    ranked = rank_documents(sim)
    assert [doc for doc, _ in ranked] == ["d1", "d2", "d5", "d10"]
    assert round(ranked[0][1], 4) == 1.0000
    assert round(ranked[1][1], 4) == 0.6147
    assert round(ranked[2][1], 4) == 0.4159
    assert round(ranked[3][1], 4) == 0.2875


def test_part_b_phrase_query_2_ground_truth(pipeline_data):
    """Phrase 2: 'sales growth' -> d3, d5, d7, d8 with exact ranking and similarity."""
    pos_index = pipeline_data["pos_index"]
    norm_tfidf = pipeline_data["norm_tfidf"]
    idf = pipeline_data["idf"]

    res = search_phrase("sales growth", pos_index)
    assert sorted(list(res.keys()), key=lambda x: int(x[1:])) == ["d3", "d5", "d7", "d8"]
    assert res["d3"] == [1]
    assert res["d5"] == [4]
    assert res["d7"] == [4]
    assert res["d8"] == [1]

    q_vec = vectorize_query(["sales", "growth"], idf)
    sim = calculate_similarity(q_vec, norm_tfidf, list(res.keys()))
    ranked = rank_documents(sim)
    assert [doc for doc, _ in ranked] == ["d5", "d3", "d8", "d7"]
    assert round(ranked[0][1], 4) == 0.4847
    assert round(ranked[1][1], 4) == 0.4395
    assert round(ranked[2][1], 4) == 0.3240
    assert round(ranked[3][1], 4) == 0.3067


def test_part_b_boolean_and_ground_truth(pipeline_data):
    """Boolean AND: 'customer service' AND 'sales growth' -> d5 only."""
    pos_index = pipeline_data["pos_index"]
    norm_tfidf = pipeline_data["norm_tfidf"]
    idf = pipeline_data["idf"]

    p1_res = search_phrase("customer service", pos_index)
    p2_res = search_phrase("sales growth", pos_index)
    and_docs = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND")
    assert and_docs == ["d5"]

    q_and_vec = vectorize_query(["customer", "service", "sales", "growth"], idf)
    sim = calculate_similarity(q_and_vec, norm_tfidf, and_docs)
    ranked = rank_documents(sim)
    assert [doc for doc, _ in ranked] == ["d5"]
    assert round(ranked[0][1], 4) == 0.6376


def test_part_b_boolean_and_not_ground_truth(pipeline_data):
    """Boolean AND NOT: 'customer service' AND NOT 'sales growth' -> d1 > d2 > d10."""
    pos_index = pipeline_data["pos_index"]
    norm_tfidf = pipeline_data["norm_tfidf"]
    idf = pipeline_data["idf"]

    p1_res = search_phrase("customer service", pos_index)
    p2_res = search_phrase("sales growth", pos_index)
    and_not_docs = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND NOT")
    assert and_not_docs == ["d1", "d2", "d10"]

    # In AND NOT: query vector built from Phrase 1 terms only
    q_p1_vec = vectorize_query(["customer", "service"], idf)
    sim = calculate_similarity(q_p1_vec, norm_tfidf, and_not_docs)
    ranked = rank_documents(sim)
    assert [doc for doc, _ in ranked] == ["d1", "d2", "d10"]
    assert round(ranked[0][1], 4) == 1.0000
    assert round(ranked[1][1], 4) == 0.6147
    assert round(ranked[2][1], 4) == 0.2875
