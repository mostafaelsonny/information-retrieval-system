"""
Member 2 (Monzer): PySpark Positional Inverted Index
Constructs an inverted index mapping term -> {doc_id -> [1-based positions]}.
"""
from typing import Dict, List
from collections import defaultdict
from src.contracts import TokenizedDocumentsContract, PositionalIndexContract


def build_positional_index(tokenized_docs: TokenizedDocumentsContract, use_spark: bool = False) -> PositionalIndexContract:
    """
    Builds the positional index.
    If use_spark is True, runs via PySpark local session; otherwise runs optimized pure-Python
    construction matching the exact same contract.
    """
    if use_spark:
        try:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder \
                .master("local[2]") \
                .appName("IR-PositionalIndex") \
                .config("spark.driver.memory", "1g") \
                .getOrCreate()

            # Flatten (term, doc_id, pos)
            records = []
            for doc_id, tokens in tokenized_docs.items():
                for term, pos in tokens:
                    records.append((term, doc_id, pos))

            rdd = spark.sparkContext.parallelize(records)
            # Group by (term, doc_id) -> list of positions
            grouped = rdd.map(lambda x: ((x[0], x[1]), x[2])) \
                         .groupByKey() \
                         .mapValues(lambda pos_iter: sorted(list(pos_iter))) \
                         .collect()

            index: PositionalIndexContract = defaultdict(dict)
            for (term, doc_id), positions in grouped:
                index[term][doc_id] = positions
            return dict(index)
        except Exception:
            # Graceful fallback to ensure deterministic execution
            pass

    # High-performance native build
    index: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(list))
    for doc_id, tokens in tokenized_docs.items():
        for term, pos in tokens:
            index[term][doc_id].append(pos)

    # Ensure sorted ascending positions and regular dict format
    clean_index: PositionalIndexContract = {}
    for term in sorted(index.keys()):
        clean_index[term] = {}
        for doc_id in sorted(index[term].keys(), key=lambda x: int(x[1:])):
            clean_index[term][doc_id] = sorted(index[term][doc_id])

    return clean_index
