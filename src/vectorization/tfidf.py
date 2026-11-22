"""
Member 4 (Rovan): TF-IDF Matrix Computation
Multiplies Weighted TF by IDF for each term and document.
"""
from typing import Dict
from src.contracts import WeightedTFContract, IDFContract, TFIDFMatrixContract


def calculate_tfidf(weighted_tf: WeightedTFContract, idf: IDFContract) -> TFIDFMatrixContract:
    """
    Calculates TF-IDF matrix:
    TF-IDF(t, d) = WTF(t, d) * IDF(t)
    """
    tfidf_matrix: TFIDFMatrixContract = {}
    for term, doc_weights in weighted_tf.items():
        term_idf = idf.get(term, 0.0)
        tfidf_matrix[term] = {}
        for doc_id, wtf in doc_weights.items():
            tfidf_matrix[term][doc_id] = wtf * term_idf
    return tfidf_matrix
