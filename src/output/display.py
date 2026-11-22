"""
Member 1 (Mostafa): Output Display & Report Exporter
Formats mathematical matrices into elegant ASCII tables and saves Part A and Part B text outputs.
"""
import os
from typing import Dict, List, Tuple


def format_table(headers: List[str], rows: List[List[str]], title: str = "") -> str:
    """Formats rows and headers into a clean fixed-width ASCII table."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(cell)))

    # Add padding
    col_widths = [w + 2 for w in col_widths]
    sep = "+" + "+".join("-" * w for w in col_widths) + "+"
    header_str = "|" + "|".join(f" {h}".ljust(w) for h, w in zip(headers, col_widths)) + "|"

    output_lines = []
    if title:
        output_lines.append(f"\n=== {title} ===")
    output_lines.append(sep)
    output_lines.append(header_str)
    output_lines.append(sep)

    for row in rows:
        row_str = "|" + "|".join(f" {str(cell)}".ljust(w) for cell, w in zip(row, col_widths)) + "|"
        output_lines.append(row_str)

    output_lines.append(sep)
    return "\n".join(output_lines)


def export_results(
    pos_index: dict,
    raw_tf: dict,
    weighted_tf: dict,
    df: dict,
    idf: dict,
    tfidf: dict,
    doc_lengths: dict,
    norm_tfidf: dict,
    p1_res: dict,
    p1_ranked: list,
    p2_res: dict,
    p2_ranked: list,
    and_res: list,
    and_ranked: list,
    and_not_res: list,
    and_not_ranked: list,
    results_dir: str = "results"
):
    """Saves Part A and Part B tables into formatted text files."""
    os.makedirs(results_dir, exist_ok=True)
    doc_ids = [f"d{i}" for i in range(1, 11)]

    # ---------------- Part A: Tables ----------------
    part_a_lines = ["=" * 80, "PART A: INDEXING, TERM STATISTICS & VECTOR MATRICES", "=" * 80]

    # Table 1: Raw TF & Weighted TF
    rows_tf = []
    for term in sorted(raw_tf.keys()):
        row = [term]
        for d in doc_ids:
            tf_val = raw_tf[term].get(d, 0)
            wtf_val = weighted_tf[term].get(d, 0.0)
            row.append(f"{tf_val} ({wtf_val:.2f})")
        rows_tf.append(row)
    part_a_lines.append(format_table(["Term"] + doc_ids, rows_tf, "Raw TF (and Weighted TF)"))

    # Table 2: DF & IDF
    rows_df = []
    for term in sorted(df.keys()):
        rows_df.append([term, str(df[term]), f"{idf[term]:.4f}"])
    part_a_lines.append(format_table(["Term", "DF", "IDF"], rows_df, "Document Frequency (DF) & IDF"))

    # Table 3: Normalized TF-IDF
    rows_norm = []
    for term in sorted(norm_tfidf.keys()):
        row = [term]
        for d in doc_ids:
            row.append(f"{norm_tfidf[term].get(d, 0.0):.4f}")
        rows_norm.append(row)
    part_a_lines.append(format_table(["Term"] + doc_ids, rows_norm, "Normalized TF-IDF Matrix (L2 Norm)"))

    with open(os.path.join(results_dir, "part_a_tables.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(part_a_lines))

    # ---------------- Part B: Queries & Ranking ----------------
    part_b_lines = ["=" * 80, "PART B: RETRIEVAL, BOOLEAN QUERIES & COSINE RANKING", "=" * 80]

    def format_rank_summary(title, docs, ranked):
        lines = [f"\n--- {title} ---", f"Matching Documents: {sorted(docs, key=lambda x: int(x[1:]))}"]
        rank_rows = [[rank, doc_id, f"{score:.4f}"] for rank, (doc_id, score) in enumerate(ranked, start=1)]
        lines.append(format_table(["Rank", "Doc ID", "Cosine Similarity"], rank_rows))
        return "\n".join(lines)

    part_b_lines.append(format_rank_summary("Phrase Query 1: 'customer service'", list(p1_res.keys()), p1_ranked))
    part_b_lines.append(format_rank_summary("Phrase Query 2: 'sales growth'", list(p2_res.keys()), p2_ranked))
    part_b_lines.append(format_rank_summary("Boolean Query: ('customer service' AND 'sales growth')", and_res, and_ranked))
    part_b_lines.append(format_rank_summary("Boolean Query: ('customer service' AND NOT 'sales growth')", and_not_res, and_not_ranked))

    with open(os.path.join(results_dir, "part_b_results.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(part_b_lines))

    print(f"✅ Outputs successfully saved to '{results_dir}/part_a_tables.txt' and '{results_dir}/part_b_results.txt'.")
