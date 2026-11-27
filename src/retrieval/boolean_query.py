"""
Member 5 (Febronia): Boolean Query Engine (IR-11)
Executes Boolean operations (AND, AND NOT) between matching document lists.
"""
from typing import List


def _natural_doc_sort_key(doc_id: str) -> tuple[int, int | str]:
    """Sort key for natural document ordering (e.g. d1, d2, ..., d10)."""
    if doc_id.startswith("d") and doc_id[1:].isdigit():
        return (0, int(doc_id[1:]))
    return (1, doc_id)


def execute_boolean_query(
    docs_p1: List[str],
    docs_p2: List[str],
    operator: str,
) -> List[str]:
    """
    Execute Boolean logic (AND or AND NOT) between two lists of matching document IDs.

    Args:
        docs_p1: Document IDs matching the first phrase query.
        docs_p2: Document IDs matching the second phrase query.
        operator: Boolean operator ('AND' or 'AND NOT' / 'NOT').

    Returns:
        Naturally sorted list of matching document IDs.

    Raises:
        ValueError: If an unsupported Boolean operator is provided.
    """
    set_a = set(docs_p1)
    set_b = set(docs_p2)
    op = " ".join(operator.strip().upper().split())

    if op == "AND":
        result_set = set_a.intersection(set_b)
    elif op in ("AND NOT", "NOT"):
        result_set = set_a.difference(set_b)
    else:
        raise ValueError(
            f"Unsupported Boolean operator: {operator}. Use 'AND' or 'AND NOT'."
        )

    return sorted(result_set, key=_natural_doc_sort_key)
