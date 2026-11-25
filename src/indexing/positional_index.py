
from collections import defaultdict
from typing import Dict, List

from src.contracts import (
    TokenizedDocumentsContract,
    PositionalIndexContract,
    validate_positional_index,
)


def build_positional_index(
    tokenized_docs: TokenizedDocumentsContract,
    use_spark: bool = False,
) -> PositionalIndexContract:
    """
    Builds a positional inverted index.

    Structure:
        term -> document_id -> [positions]

    Positions are 1-based and sorted in ascending order.

    Args:
        tokenized_docs: Tokenized documents using (term, position) tuples.
        use_spark: Whether to use PySpark for index construction.

    Returns:
        A positional inverted index matching PositionalIndexContract.
    """

    if use_spark:
        index = _build_with_spark(tokenized_docs)
    else:
        index = _build_with_python(tokenized_docs)

    validate_positional_index(index)

    return index


def _build_with_python(
    tokenized_docs: TokenizedDocumentsContract,
) -> PositionalIndexContract:
    """Builds the positional index using native Python."""

    index = defaultdict(lambda: defaultdict(list))

    for doc_id, tokens in tokenized_docs.items():
        for term, position in tokens:
            index[term][doc_id].append(position)

    return {
        term: {
            doc_id: sorted(index[term][doc_id])
            for doc_id in sorted(
                index[term],
                key=lambda item: int(item[1:]),
            )
        }
        for term in sorted(index)
    }


def _build_with_spark(
    tokenized_docs: TokenizedDocumentsContract,
) -> PositionalIndexContract:
    """Builds the positional index using PySpark RDD operations."""

    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("IR-PositionalIndex")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.memory", "1g")
        .getOrCreate()
    )

    records = [
        (term, doc_id, position)
        for doc_id, tokens in tokenized_docs.items()
        for term, position in tokens
    ]

    rdd = spark.sparkContext.parallelize(records)

    grouped = (
        rdd
        .map(lambda record: (
            (record[0], record[1]),
            [record[2]],
        ))
        .reduceByKey(lambda left, right: left + right)
        .mapValues(sorted)
        .map(lambda item: (
            item[0][0],
            (item[0][1], item[1]),
        ))
        .groupByKey()
        .collect()
    )

    index = {
        term: {
            doc_id: positions
            for doc_id, positions in sorted(
                postings,
                key=lambda item: int(item[0][1:]),
            )
        }
        for term, postings in sorted(grouped, key=lambda item: item[0])
    }

    return index
