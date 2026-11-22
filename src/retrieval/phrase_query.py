"""
Member 5 (Febronia): Phrase Query Engine
Searches for exact consecutive word sequences using the positional index.
"""
from typing import Dict, List
from src.contracts import PositionalIndexContract, PhraseResultsContract


def search_phrase(phrase: str, pos_index: PositionalIndexContract) -> Dict[str, List[int]]:
    """
    Finds documents containing the exact phrase, where word positions are strictly consecutive (pos2 = pos1 + 1).
    Returns mapping: {doc_id -> [match_starting_positions]}
    """
    terms = phrase.strip().lower().split()
    if not terms:
        return {}

    # Single term query
    if len(terms) == 1:
        term = terms[0]
        return {doc_id: list(positions) for doc_id, positions in pos_index.get(term, {}).items()}

    # Multi-term phrase query
    first_term = terms[0]
    if first_term not in pos_index:
        return {}

    matching_docs: Dict[str, List[int]] = {}

    for doc_id, start_positions in pos_index[first_term].items():
        valid_start_positions: List[int] = []

        for start_pos in start_positions:
            is_match = True
            for offset, next_term in enumerate(terms[1:], start=1):
                expected_pos = start_pos + offset
                doc_positions = pos_index.get(next_term, {}).get(doc_id, [])
                if expected_pos not in doc_positions:
                    is_match = False
                    break
            if is_match:
                valid_start_positions.append(start_pos)

        if valid_start_positions:
            matching_docs[doc_id] = valid_start_positions

    return matching_docs
