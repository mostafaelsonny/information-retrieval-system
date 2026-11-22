"""
Member 3 (Ebrahim): Information Statistics
Calculates Raw TF, Weighted TF, Document Frequency (DF), and Inverse Document Frequency (IDF).
Rules: Base-10 logarithm, WTF = 1 + log10(TF) when TF > 0 else 0.0, IDF = log10(N / DF).
"""
import math
from typing import Dict
from src.contracts import PositionalIndexContract, RawTFContract, WeightedTFContract, DFContract, IDFContract


def calculate_raw_tf(pos_index: PositionalIndexContract) -> RawTFContract:
    """Calculates term frequency as the count of occurrences (positions) in each document."""
    raw_tf: RawTFContract = {}
    for term, postings in pos_index.items():
        raw_tf[term] = {}
        for doc_id, positions in postings.items():
            raw_tf[term][doc_id] = len(positions)
    return raw_tf


def calculate_weighted_tf(raw_tf: RawTFContract) -> WeightedTFContract:
    """
    Calculates weighted term frequency:
    WTF = 1 + log10(TF) if TF > 0 else 0.0
    """
    weighted_tf: WeightedTFContract = {}
    for term, doc_counts in raw_tf.items():
        weighted_tf[term] = {}
        for doc_id, count in doc_counts.items():
            weighted_tf[term][doc_id] = (1.0 + math.log10(count)) if count > 0 else 0.0
    return weighted_tf


def calculate_df(pos_index: PositionalIndexContract) -> DFContract:
    """Calculates document frequency: count of documents containing the term."""
    df: DFContract = {}
    for term, postings in pos_index.items():
        df[term] = len(postings.keys())
    return df


def calculate_idf(df: DFContract, total_documents: int = 10) -> IDFContract:
    """
    Calculates inverse document frequency:
    IDF = log10(total_documents / DF)
    """
    idf: IDFContract = {}
    for term, doc_freq in df.items():
        idf[term] = math.log10(total_documents / doc_freq)
    return idf
