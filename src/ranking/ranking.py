"""
Member 5 (Febronia): Document Ranking Engine
Sorts matching documents descendingly by their cosine similarity score.
"""
from typing import Dict, List, Tuple


def rank_documents(similarity_scores: Dict[str, float]) -> List[Tuple[str, float]]:
    """
    Ranks documents by similarity score in descending order.
    Returns list of tuples: [("d1", 1.0000), ("d2", 0.6147), ...]
    """
    return sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)
