"""
Member 5 (Febronia): Cosine Similarity Calculator
Computes cosine similarity between normalized query vector and normalized document vectors.
Since vectors are L2-normalized, Cosine Similarity is simply the Dot Product!
"""
from typing import Dict, List
from src.contracts import QueryVectorContract, NormalizedTFIDFContract


def calculate_similarity(
    query_vector: QueryVectorContract,
    normalized_tfidf: NormalizedTFIDFContract,
    target_docs: List[str]
) -> Dict[str, float]:
    """
    Calculates cosine similarity for target documents:
    Sim(Q, D) = sum( q_weight * doc_weight for all terms in Q )
    Returns mapping: {doc_id -> similarity_score}
    """
    scores: Dict[str, float] = {}
    for doc_id in target_docs:
        dot_product = 0.0
        for term, q_weight in query_vector.items():
            doc_weight = normalized_tfidf.get(term, {}).get(doc_id, 0.0)
            dot_product += q_weight * doc_weight
        scores[doc_id] = dot_product
    return scores
