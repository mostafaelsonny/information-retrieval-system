"""
Member 1 (Mostafa): Main Orchestration Pipeline
Executes the end-to-end IR System pipeline across all modules.
"""
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessing.document_loader import load_documents
from src.preprocessing.tokenizer import tokenize_documents
from src.indexing.positional_index import build_positional_index
from src.statistics.term_statistics import calculate_raw_tf, calculate_weighted_tf, calculate_df, calculate_idf
from src.vectorization.tfidf import calculate_tfidf
from src.vectorization.normalization import calculate_document_lengths, normalize_tfidf, vectorize_query
from src.retrieval.phrase_query import search_phrase
from src.retrieval.boolean_query import execute_boolean_query
from src.ranking.similarity import calculate_similarity
from src.ranking.ranking import rank_documents
from src.output.display import export_results


def run_pipeline(data_dir: str = "data"):
    print("=" * 70)
    print("🚀 Running Information Storage & Retrieval (IR) System Pipeline")
    print("=" * 70)

    # 1. Load Documents
    print("📂 Step 1: Loading documents from disk...")
    docs = load_documents(data_dir)
    print(f"   Loaded {len(docs)} documents.")

    # 2. Tokenize Documents
    print("✂️ Step 2: Tokenizing documents with 1-based sequential positions...")
    tokenized = tokenize_documents(docs)

    # 3. Build Positional Inverted Index
    print("📇 Step 3: Constructing Positional Inverted Index...")
    pos_index = build_positional_index(tokenized, use_spark=False)
    print(f"   Indexed {len(pos_index)} unique vocabulary terms.")

    # 4. Term Statistics
    print("📊 Step 4: Computing Raw TF, Weighted TF, DF, and IDF...")
    raw_tf = calculate_raw_tf(pos_index)
    weighted_tf = calculate_weighted_tf(raw_tf)
    df = calculate_df(pos_index)
    idf = calculate_idf(df, total_documents=len(docs))

    # 5. Vector Space Model & Normalization
    print("📐 Step 5: Generating TF-IDF matrix and applying L2 Normalization...")
    tfidf = calculate_tfidf(weighted_tf, idf)
    doc_lengths = calculate_document_lengths(tfidf, list(docs.keys()))
    norm_tfidf = normalize_tfidf(tfidf, doc_lengths)

    # 6. Phrase Queries
    print("🔍 Step 6: Executing Phrase Queries...")
    p1 = "customer service"
    p2 = "sales growth"
    p1_res = search_phrase(p1, pos_index)
    p2_res = search_phrase(p2, pos_index)
    print(f"   Phrase 1 ('{p1}'): {sorted(p1_res.keys(), key=lambda x: int(x[1:]))}")
    print(f"   Phrase 2 ('{p2}'): {sorted(p2_res.keys(), key=lambda x: int(x[1:]))}")

    # 7. Boolean Queries
    print("⚡ Step 7: Executing Boolean Logic Queries...")
    and_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND")
    and_not_res = execute_boolean_query(list(p1_res.keys()), list(p2_res.keys()), "AND NOT")
    print(f"   AND Query ('{p1}' AND '{p2}'): {and_res}")
    print(f"   AND NOT Query ('{p1}' AND NOT '{p2}'): {and_not_res}")

    # 8. Cosine Similarity & Ranking
    print("🎯 Step 8: Computing Cosine Similarity and Document Rankings...")
    # Ranking for Phrase 1
    q1_vec = vectorize_query(p1.split(), idf)
    sim_p1 = calculate_similarity(q1_vec, norm_tfidf, list(p1_res.keys()))
    p1_ranked = rank_documents(sim_p1)

    # Ranking for Phrase 2
    q2_vec = vectorize_query(p2.split(), idf)
    sim_p2 = calculate_similarity(q2_vec, norm_tfidf, list(p2_res.keys()))
    p2_ranked = rank_documents(sim_p2)

    # Ranking for AND
    q_and_vec = vectorize_query((p1 + " " + p2).split(), idf)
    sim_and = calculate_similarity(q_and_vec, norm_tfidf, and_res)
    and_ranked = rank_documents(sim_and)

    # Ranking for AND NOT (Vectorized exclusively from Phrase 1 terms)
    q_and_not_vec = vectorize_query(p1.split(), idf)
    sim_and_not = calculate_similarity(q_and_not_vec, norm_tfidf, and_not_res)
    and_not_ranked = rank_documents(sim_and_not)

    # 9. Export Results
    print("💾 Step 9: Exporting Part A & Part B deliverables...")
    export_results(
        pos_index, raw_tf, weighted_tf, df, idf, tfidf, doc_lengths, norm_tfidf,
        p1_res, p1_ranked, p2_res, p2_ranked, and_res, and_ranked, and_not_res, and_not_ranked
    )

    print("=" * 70)
    print("🎉 Pipeline executed successfully End-to-End!")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
