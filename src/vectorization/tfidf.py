"""
Member 4 (Rovan): TF-IDF Matrix Computation (IR-07)
Multiplies Weighted TF by IDF for each term and document while preserving full
64-bit floating-point precision (no intermediate rounding).
"""
from src.contracts import IDFContract, TFIDFMatrixContract, WeightedTFContract


def calculate_tfidf(
    weighted_tf: WeightedTFContract,
    idf: IDFContract,
) -> TFIDFMatrixContract:
    """
    Calculates the TF-IDF weighting matrix for all terms and documents:
        TF-IDF(t, d) = WTF(t, d) * IDF(t)

    Args:
        weighted_tf: Mapping of term -> {doc_id -> weighted term frequency}.
        idf: Mapping of term -> inverse document frequency.

    Returns:
        Mapping of term -> {doc_id -> TF-IDF weight} with full float precision.
    """
    tfidf_matrix: TFIDFMatrixContract = {}
    for term, doc_weights in weighted_tf.items():
        term_idf = float(idf.get(term, 0.0))
        tfidf_matrix[term] = {
            doc_id: float(wtf) * term_idf
            for doc_id, wtf in doc_weights.items()
        }
    return tfidf_matrix

