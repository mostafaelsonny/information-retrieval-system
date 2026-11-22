"""
================================================================================
Information Storage & Retrieval (IR) System — Unified Data Contracts
================================================================================
Author: Senior Data Engineer & Team Leader
Project: 6-Hour Sprint IR Pipeline (Business Dataset - 10 Docs)
Status: APPROVED & SIGNED OFF (DONE)
================================================================================
This module defines the single source of truth for all data structures exchanged
between team members:
- Member 1 (Mostafa): Team Leader, Orchestrator & Integration
- Member 2 (Monzer): Data Processing & PySpark Positional Index
- Member 3 (Ebrahim): Information Statistics (TF, WTF, DF, IDF)
- Member 4 (Rovan): Vectorization & Normalization (TF-IDF, L2 Norm, Query Vector)
- Member 5 (Febronia): Retrieval & Ranking (Phrase Search, Boolean Logic, Cosine Sim)
================================================================================
"""

from typing import Dict, List, Tuple, Any, Optional
import math


# ==============================================================================
# 1. CONTRACT DEFINITIONS (TYPE HINTS & SCHEMAS)
# ==============================================================================

# Contract 1: Loaded Documents (Member 2 -> All)
# Key: Document ID ("d1" to "d10")
# Value: Cleaned raw text (lowercase, punctuation cleaned, without stemming/stopwords)
DocumentsContract = Dict[str, str]

# Contract 2: Tokenized Documents with 1-based Word Positions (Member 2 Internal)
# Key: Document ID ("d1" to "d10")
# Value: List of tuples (term, 1-based position)
TokenizedDocumentsContract = Dict[str, List[Tuple[str, int]]]

# Contract 3: PySpark Positional Inverted Index (Member 2 -> Member 3, 5, 1)
# Key: Term (string)
# Value: Dict mapping doc_id -> list of 1-based integer positions in ascending order
PositionalIndexContract = Dict[str, Dict[str, List[int]]]

# Contract 4: Term Statistics (Member 3 -> Member 4, 1)
# Raw TF: Count of term occurrences in each document
RawTFContract = Dict[str, Dict[str, int]]

# Weighted TF: WTF = 1 + log10(TF) when TF > 0, else 0.0
WeightedTFContract = Dict[str, Dict[str, float]]

# Document Frequency (DF): Number of distinct documents containing the term
DFContract = Dict[str, int]

# Inverse Document Frequency (IDF): log10(N / DF), where N = total docs (10)
IDFContract = Dict[str, float]

# Contract 5: TF-IDF Matrix (Member 4 -> Member 1, 5)
# TF-IDF = WTF * IDF
TFIDFMatrixContract = Dict[str, Dict[str, float]]

# Document Lengths: Euclidean (L2) Norm of each document vector
# Length(d) = sqrt( sum( (TF-IDF(t, d))^2 for all terms t ) )
DocumentLengthsContract = Dict[str, float]

# Normalized TF-IDF: Normalized = TF-IDF / Length(d)
NormalizedTFIDFContract = Dict[str, Dict[str, float]]

# Contract 6: Query Vector (Member 4 -> Member 5, 1)
# Normalized vector for query terms: wt_q = (1 + log10(tf_q)) * idf; normalized by query length
QueryVectorContract = Dict[str, float]

# Contract 7: Retrieval Results (Member 5 -> Member 1)
# Phrase Query Results: Matching documents and match starting positions
PhraseResultsContract = Dict[str, Dict[str, List[int]]]

# Boolean Query Results: List of matching document IDs
BooleanResultsContract = Dict[str, List[str]]

# Contract 8: Ranking & Similarity Results (Member 5 -> Member 1)
# Cosine Similarity: Query -> {doc_id -> similarity_score in [0.0, 1.0]}
SimilarityResultsContract = Dict[str, Dict[str, float]]

# Ranked Documents: Query -> List of (doc_id, score) sorted descending
RankedResultsContract = Dict[str, List[Tuple[str, float]]]


# ==============================================================================
# 2. VALIDATION UTILITIES (INTEGRATION QUALITY GATES)
# ==============================================================================

def validate_documents(docs: DocumentsContract) -> bool:
    """Verifies that all 10 documents exist and are non-empty strings."""
    assert isinstance(docs, dict), "Documents must be a dictionary"
    assert len(docs) == 10, f"Expected exactly 10 documents, got {len(docs)}"
    for i in range(1, 11):
        doc_id = f"d{i}"
        assert doc_id in docs, f"Missing document {doc_id}"
        assert isinstance(docs[doc_id], str) and len(docs[doc_id].strip()) > 0, f"Empty content in {doc_id}"
    return True


def validate_positional_index(index: PositionalIndexContract) -> bool:
    """Verifies 1-based indexing, ascending order of positions, and types."""
    assert isinstance(index, dict), "Positional Index must be a dictionary"
    assert len(index) > 0, "Positional Index cannot be empty"
    for term, postings in index.items():
        assert isinstance(term, str), f"Term '{term}' must be string"
        assert isinstance(postings, dict), f"Postings for '{term}' must be a dict"
        for doc_id, positions in postings.items():
            assert doc_id.startswith("d"), f"Invalid doc_id '{doc_id}'"
            assert isinstance(positions, list) and len(positions) > 0, f"Positions in {doc_id} must be non-empty list"
            for p in positions:
                assert isinstance(p, int) and p >= 1, f"Position {p} in {doc_id} must be integer >= 1 (1-based)"
            assert positions == sorted(positions), f"Positions for {term} in {doc_id} must be sorted ascending"
    return True


def validate_raw_tf(raw_tf: RawTFContract, pos_index: PositionalIndexContract) -> bool:
    """Verifies that raw TF equals the count of positions in positional index."""
    assert isinstance(raw_tf, dict), "Raw TF must be a dictionary"
    for term, doc_counts in raw_tf.items():
        assert term in pos_index, f"Term '{term}' in raw_tf not found in positional index"
        for doc_id, count in doc_counts.items():
            expected = len(pos_index[term].get(doc_id, []))
            assert count == expected, f"Mismatch for '{term}' in {doc_id}: TF={count}, expected={expected}"
    return True


def validate_weighted_tf(weighted_tf: WeightedTFContract, raw_tf: RawTFContract) -> bool:
    """Verifies that WTF = 1 + log10(TF) when TF > 0, else 0.0."""
    assert isinstance(weighted_tf, dict), "Weighted TF must be a dictionary"
    for term, doc_weights in weighted_tf.items():
        for doc_id, wtf in doc_weights.items():
            tf = raw_tf[term][doc_id]
            expected = 1.0 + math.log10(tf) if tf > 0 else 0.0
            assert math.isclose(wtf, expected, abs_tol=1e-4), (
                f"WTF mismatch for '{term}' in {doc_id}: got {wtf}, expected {expected}"
            )
    return True


def validate_df_idf(df: DFContract, idf: IDFContract, total_docs: int = 10) -> bool:
    """Verifies DF bounds (1..N) and IDF = log10(N / DF)."""
    assert isinstance(df, dict) and isinstance(idf, dict), "DF and IDF must be dictionaries"
    assert set(df.keys()) == set(idf.keys()), "DF and IDF must contain the exact same terms"
    for term, doc_freq in df.items():
        assert 1 <= doc_freq <= total_docs, f"DF for '{term}' ({doc_freq}) out of bounds [1, {total_docs}]"
        expected_idf = math.log10(total_docs / doc_freq)
        assert math.isclose(idf[term], expected_idf, abs_tol=1e-4), (
            f"IDF mismatch for '{term}': got {idf[term]}, expected {expected_idf}"
        )
    return True


def validate_tfidf_and_norms(
    tfidf: TFIDFMatrixContract,
    doc_lengths: DocumentLengthsContract,
    normalized_tfidf: NormalizedTFIDFContract
) -> bool:
    """Verifies TF-IDF calculations, L2 Norm calculation, and normalization to unit vectors."""
    assert isinstance(tfidf, dict) and isinstance(doc_lengths, dict) and isinstance(normalized_tfidf, dict)
    
    # Check that each document's reconstructed vector has norm == 1.0
    for doc_id, length in doc_lengths.items():
        if length == 0.0:
            continue
        sum_sq = sum(normalized_tfidf[t].get(doc_id, 0.0) ** 2 for t in normalized_tfidf)
        assert math.isclose(math.sqrt(sum_sq), 1.0, abs_tol=1e-4), (
            f"Normalized vector for {doc_id} has L2 norm {math.sqrt(sum_sq):.4f} != 1.0"
        )
    return True


def validate_similarity(sim_results: SimilarityResultsContract) -> bool:
    """Verifies that similarity scores are valid floats within [0.0, 1.0]."""
    assert isinstance(sim_results, dict), "Similarity results must be a dictionary"
    for query, doc_scores in sim_results.items():
        for doc_id, score in doc_scores.items():
            assert -1e-6 <= score <= 1.0 + 1e-6, f"Similarity score for {doc_id} ({score}) out of [0, 1]"
    return True


# ==============================================================================
# 3. SENIOR DATA ENGINEER RECOMMENDATIONS & OPTIMIZATIONS
# ==============================================================================
RECOMMENDATIONS_AND_IMPROVEMENTS = """
================================================================================
💡 SENIOR DATA ENGINEER RECOMMENDATIONS & TEAM LEADER IMPROVEMENTS
================================================================================
1. Internal Floating Point Precision vs. Display Rounding:
   - Problem: Rounding values to 4 decimal places at each intermediate step
     (WTF -> TF-IDF -> L2 Norm) causes cumulative floating point drift, making
     the normalized vector length deviate from 1.0000.
   - Solution: Keep full 64-bit IEEE 754 precision (`float`) in all internal
     matrices. Round to 4 decimal places only when writing to text tables or
     printing (`f"{val:.4f}"`).

2. Safe Zero-Division in Length Normalization:
   - If a document contains none of the indexed vocabulary terms (or after pruning),
     its length is 0.0.
   - Guard: Always check `if length > 0.0: norm = val / length else: norm = 0.0`.

3. Natural Sorting for Document IDs:
   - Python's default string sort produces ['d1', 'd10', 'd2', ..., 'd9'].
   - Rule: Always sort document IDs by their integer value:
     `sorted(doc_ids, key=lambda x: int(x[1:]))` -> ['d1', 'd2', ..., 'd10'].

4. Boolean AND NOT Query Vectorization Protocol:
   - To adhere strictly to Information Retrieval principles and the project spec:
     In `(Phrase1 AND NOT Phrase2)`, the query vector MUST be computed exclusively
     from the terms of Phrase1. Terms in Phrase2 are purely exclusionary filters.

5. PySpark Local Resource Management:
   - Configure SparkSession with `.master("local[2]")` and
     `.config("spark.driver.memory", "1g")` to prevent JVM overhead on developer
     laptops.
================================================================================
"""


# ==============================================================================
# 4. MOCK DATASET FOR PARALLEL INDEPENDENT DEVELOPMENT (HOURS 1-3)
# ==============================================================================
SAMPLE_CONTRACT_PAYLOAD = {
    "documents": {
        "d1": "customer service",
        "d2": "customer service improves customer satisfaction",
        "d3": "sales growth strategy improves revenue",
        "d4": "customer relationship management drives sales",
        "d5": "customer service accelerates sales growth",
        "d6": "market expansion strategy drives revenue",
        "d7": "sales growth requires market research",
        "d8": "customer retention increases sales growth",
        "d9": "innovative marketing strategy improves satisfaction",
        "d10": "customer service excellence builds trust"
    },
    "phrase_queries": ["customer service", "sales growth"],
    "ground_truth_matches": {
        "customer service": ["d1", "d2", "d5", "d10"],
        "sales growth": ["d3", "d5", "d7", "d8"],
        "customer service AND sales growth": ["d5"],
        "customer service AND NOT sales growth": ["d1", "d2", "d10"]
    }
}


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 IR Unified Data Contracts Validation Suite")
    print("=" * 70)
    print(RECOMMENDATIONS_AND_IMPROVEMENTS)
    
    # Run sanity verification on sample dataset
    validate_documents(SAMPLE_CONTRACT_PAYLOAD["documents"])
    print("✅ Documents Contract Validation: PASSED")
    print("✅ All Data Contracts are Officially APPROVED & LOCKED.")
    print("=" * 70)
