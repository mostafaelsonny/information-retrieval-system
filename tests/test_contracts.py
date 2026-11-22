"""
Validates that the project adheres to all Data Contracts schemas and rules.
"""
import math
from src.contracts import (
    validate_documents,
    validate_positional_index,
    validate_raw_tf,
    validate_weighted_tf,
    validate_df_idf,
    validate_tfidf_and_norms,
    validate_similarity,
    SAMPLE_CONTRACT_PAYLOAD
)
from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.indexing.positional_index import build_positional_index
from src.statistics.term_statistics import calculate_raw_tf, calculate_weighted_tf, calculate_df, calculate_idf
from src.vectorization.tfidf import calculate_tfidf
from src.vectorization.normalization import calculate_document_lengths, normalize_tfidf


def test_sample_contracts_payload():
    assert validate_documents(SAMPLE_CONTRACT_PAYLOAD["documents"]) is True


def test_pipeline_contracts_integrity():
    docs = load_documents("data")
    assert validate_documents(docs) is True

    tokens = tokenize_documents(docs)
    pos_index = build_positional_index(tokens)
    assert validate_positional_index(pos_index) is True

    raw_tf = calculate_raw_tf(pos_index)
    assert validate_raw_tf(raw_tf, pos_index) is True

    weighted_tf = calculate_weighted_tf(raw_tf)
    assert validate_weighted_tf(weighted_tf, raw_tf) is True

    df = calculate_df(pos_index)
    idf = calculate_idf(df, total_documents=len(docs))
    assert validate_df_idf(df, idf, total_docs=len(docs)) is True

    tfidf = calculate_tfidf(weighted_tf, idf)
    doc_lengths = calculate_document_lengths(tfidf, list(docs.keys()))
    norm_tfidf = normalize_tfidf(tfidf, doc_lengths)
    assert validate_tfidf_and_norms(tfidf, doc_lengths, norm_tfidf) is True
