"""
Member 5 (Febronia): Document Ranking Engine (IR-12)
Sorts matching documents descendingly by their cosine similarity score,
breaking ties naturally by ascending document ID.
"""
from typing import Dict, List, Tuple


def _natural_doc_sort_key(doc_id: str) -> Tuple[int, int | str]:
    """Sort key for natural ascending document ordering (e.g. d1, d2, ..., d10)."""
    if doc_id.startswith("d") and doc_id[1:].isdigit():
        return (0, int(doc_id[1:]))
    return (1, doc_id)


def rank_documents(similarity_scores: Dict[str, float]) -> List[Tuple[str, float]]:
    """
    Rank documents in descending order of similarity score.

    Ties in similarity score are broken in ascending natural document ID order.

    Args:
        similarity_scores: Mapping of doc_id -> similarity score.

    Returns:
        Sorted list of (doc_id, score) tuples.
    """
    return sorted(
        similarity_scores.items(),
        key=lambda item: (-item[1], _natural_doc_sort_key(item[0])),
    )
