"""
Member 4 (Rovan): Vector Normalization & Query Vectorizer (IR-08 & IR-09)
Calculates Euclidean (L2) document lengths, normalizes document vectors to unit length (1.0),
and normalizes query vectors.
"""
import math
from collections import Counter
from typing import Dict, List

from src.contracts import (
    DocumentLengthsContract,
    IDFContract,
    NormalizedTFIDFContract,
    QueryVectorContract,
    TFIDFMatrixContract,
)


def calculate_document_lengths(
    tfidf_matrix: TFIDFMatrixContract,
    doc_ids: List[str],
) -> DocumentLengthsContract:
    """
    Calculates L2 Euclidean length for each document:
        |D| = sqrt( sum( TF-IDF(t, D)^2 for all terms t ) )

    Preserves full 64-bit floating-point precision with no intermediate rounding.
    """
    lengths: DocumentLengthsContract = {doc_id: 0.0 for doc_id in doc_ids}
    for doc_scores in tfidf_matrix.values():
        for doc_id in lengths:
            weight = float(doc_scores.get(doc_id, 0.0))
            lengths[doc_id] += weight ** 2

    for doc_id in lengths:
        lengths[doc_id] = math.sqrt(lengths[doc_id])
    return lengths


def normalize_tfidf(
    tfidf_matrix: TFIDFMatrixContract,
    document_lengths: DocumentLengthsContract,
) -> NormalizedTFIDFContract:
    """
    Applies L2 normalization to the TF-IDF matrix by dividing each weight
    by its document Euclidean length:
        Normalized(t, D) = TF-IDF(t, D) / |D|

    Returns a complete matrix covering all documents in `document_lengths`.
    Safe division: if |D| <= 0.0, normalized weight is set to 0.0.
    """
    norm_matrix: NormalizedTFIDFContract = {}
    for term, doc_scores in tfidf_matrix.items():
        all_doc_ids = list(
            dict.fromkeys(list(document_lengths.keys()) + list(doc_scores.keys()))
        )
        norm_matrix[term] = {}
        for doc_id in all_doc_ids:
            weight = float(doc_scores.get(doc_id, 0.0))
            length = float(document_lengths.get(doc_id, 0.0))
            norm_matrix[term][doc_id] = (weight / length) if length > 0.0 else 0.0
    return norm_matrix


def vectorize_query(query_terms: List[str], idf: IDFContract) -> QueryVectorContract:
    """
    Constructs a normalized query vector:
    1. Raw TF = count of each term in query
    2. WTF = 1 + log10(TF)
    3. Weight = WTF * IDF
    4. Normalize by query vector Euclidean length
    """
    term_counts = Counter(query_terms)
    unnormalized_weights: Dict[str, float] = {}

    for term, count in term_counts.items():
        term_idf = idf.get(term, 0.0)
        wtf = 1.0 + math.log10(count) if count > 0 else 0.0
        unnormalized_weights[term] = wtf * term_idf

    q_length = math.sqrt(sum(w ** 2 for w in unnormalized_weights.values()))

    normalized_query: QueryVectorContract = {}
    for term, weight in unnormalized_weights.items():
        normalized_query[term] = (weight / q_length) if q_length > 0.0 else 0.0
    return normalized_query
