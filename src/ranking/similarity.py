"""
Member 5 (Febronia): Cosine Similarity Calculator (IR-12)
Computes cosine similarity between the L2-normalized query vector and
L2-normalized document vectors for retrieved matching documents only.
"""
from typing import Dict, List

from src.contracts import NormalizedTFIDFContract, QueryVectorContract


def calculate_similarity(
    query_vector: QueryVectorContract,
    normalized_tfidf: NormalizedTFIDFContract,
    target_docs: List[str],
) -> Dict[str, float]:
    """
    Calculate Cosine Similarity via Dot Product between an L2-normalized query
    vector and each L2-normalized document vector in target_docs.

    Sim(Q, D) = sum(q_weight * doc_weight for term, q_weight in query_vector.items())

    Args:
        query_vector: L2-normalized query vector mapping term -> weight.
        normalized_tfidf: Normalized TF-IDF matrix mapping term -> {doc_id -> weight}.
        target_docs: List of retrieved matching document IDs to score.

    Returns:
        Dictionary mapping each target doc_id to its cosine similarity score.
    """
    scores: Dict[str, float] = {}
    for doc_id in target_docs:
        dot_product = 0.0
        for term, q_weight in query_vector.items():
            doc_weight = normalized_tfidf.get(term, {}).get(doc_id, 0.0)
            dot_product += q_weight * doc_weight
        scores[doc_id] = dot_product
    return scores
