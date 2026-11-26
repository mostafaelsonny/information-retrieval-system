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
    Converts query terms into an L2-normalized TF-IDF vector using collection IDF:
        1. Normalize tokens (lowercase, strip whitespace, skip empty) and compute Raw TF.
        2. Apply logarithmic TF weighting: WTF = 1.0 + log10(TF).
        3. Multiply by collection IDF (never recompute IDF from the query).
        4. Compute Euclidean (L2) query vector length: |Q| = sqrt(sum(weight^2)).
        5. Return normalized query vector Q_norm (0.0 safely when |Q| == 0.0).
    """
    raw_tf: Dict[str, int] = {}
    for token in query_terms:
        clean_token = token.lower().strip()
        if not clean_token:
            continue
        raw_tf[clean_token] = raw_tf.get(clean_token, 0) + 1

    query_tfidf: Dict[str, float] = {}
    sum_sq = 0.0
    for token, tf in raw_tf.items():
        wtf = 1.0 + math.log10(tf)
        token_idf = float(idf.get(token, 0.0))
        weight = wtf * token_idf
        query_tfidf[token] = weight
        sum_sq += weight ** 2

    q_length = math.sqrt(sum_sq)

    normalized_query: QueryVectorContract = {}
    for token, weight in query_tfidf.items():
        normalized_query[token] = (weight / q_length) if q_length > 0.0 else 0.0
    return normalized_query

