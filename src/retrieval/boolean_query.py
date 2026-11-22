"""
Member 5 (Febronia): Boolean Query Engine
Executes Boolean operations (AND, AND NOT) between matching document lists.
"""
from typing import List


def execute_boolean_query(docs_p1: List[str], docs_p2: List[str], operator: str) -> List[str]:
    """
    Executes Boolean logic between two lists of document IDs.
    - AND: Set intersection (documents in both lists)
    - AND NOT: Set difference (documents in docs_p1 but NOT in docs_p2)
    Returns sorted list of matching document IDs.
    """
    set1 = set(docs_p1)
    set2 = set(docs_p2)
    op = operator.strip().upper()

    if op == "AND":
        result = set1.intersection(set2)
    elif op in ("AND NOT", "NOT"):
        result = set1.difference(set2)
    else:
        raise ValueError(f"Unsupported Boolean operator: {operator}. Use 'AND' or 'AND NOT'.")

    return sorted(list(result), key=lambda x: int(x[1:]))
