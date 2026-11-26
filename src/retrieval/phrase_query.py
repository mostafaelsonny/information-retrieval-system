"""
Member 5 (Febronia): Positional Phrase Query Engine (IR-10)
Searches for exact consecutive word sequences using the positional inverted index.
"""
from typing import Dict, List

from src.contracts import PositionalIndexContract


def search_phrase(
    phrase: str,
    positional_index: PositionalIndexContract,
) -> Dict[str, List[int]]:
    """
    Search for an exact phrase of one or more terms in the positional index.

    For multi-word phrases, verifies strictly consecutive 1-based positions
    such that Position(word_{i+1}) == Position(word_i) + 1.

    Args:
        phrase: Search query string.
        positional_index: Mapping of term -> {doc_id -> sorted list of 1-based positions}.

    Returns:
        Dictionary mapping each matching doc_id (naturally sorted) to its list
        of matching starting positions.
    """
    words = phrase.lower().strip().split()
    if not words:
        return {}

    if len(words) == 1:
        term = words[0]
        postings = positional_index.get(term, {})
        return {
            doc_id: list(postings[doc_id])
            for doc_id in sorted(
                postings.keys(),
                key=lambda x: (0, int(x[1:])) if x.startswith("d") and x[1:].isdigit() else (1, x),
            )
        }

    first_term = words[0]
    first_postings = positional_index.get(first_term, {})
    if not first_postings:
        return {}

    candidate_docs = set(first_postings.keys())
    for word in words[1:]:
        candidate_docs.intersection_update(positional_index.get(word, {}).keys())

    if not candidate_docs:
        return {}

    results: Dict[str, List[int]] = {}
    for doc_id in sorted(
        candidate_docs,
        key=lambda x: (0, int(x[1:])) if x.startswith("d") and x[1:].isdigit() else (1, x),
    ):
        first_positions = first_postings[doc_id]
        next_position_sets = [
            set(positional_index.get(next_word, {}).get(doc_id, []))
            for next_word in words[1:]
        ]
        matching_starts: List[int] = []

        for start_pos in first_positions:
            if all(
                (start_pos + offset) in pos_set
                for offset, pos_set in enumerate(next_position_sets, start=1)
            ):
                matching_starts.append(start_pos)

        if matching_starts:
            results[doc_id] = matching_starts

    return results
