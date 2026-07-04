# test_final_state.py

import os
import math
import csv
import pytest

def compute_expected_recommendations():
    docs = [
        ("doc1", "deep learning for computer vision"),
        ("doc2", "natural language processing with deep learning"),
        ("doc3", "computer vision applications in robotics"),
        ("doc4", "robotics and control systems"),
        ("doc5", "natural language processing and text mining")
    ]

    doc_tokens = [d[1].split() for d in docs]
    # The rust code iterates over a HashSet to build vocab, which means order is non-deterministic.
    # However, cosine similarity is independent of vector dimension ordering.
    vocab = list(set([t for tokens in doc_tokens for t in tokens]))

    n_docs = len(docs)
    idf = {}
    for term in vocab:
        df = sum(1 for tokens in doc_tokens if term in tokens)
        idf[term] = math.log(n_docs / df)

    tfidf_matrix = []
    for tokens in doc_tokens:
        vec = []
        total_terms = len(tokens)
        term_counts = {t: tokens.count(t) for t in set(tokens)}
        for term in vocab:
            count = term_counts.get(term, 0)
            tf = count / total_terms
            vec.append(tf * idf[term])
        tfidf_matrix.append(vec)

    def cosine_sim(v1, v2):
        dot = sum(a*b for a,b in zip(v1, v2))
        norm1 = math.sqrt(sum(a*a for a in v1))
        norm2 = math.sqrt(sum(a*a for a in v2))
        if norm1 == 0 or norm2 == 0: return 0.0
        return dot / (norm1 * norm2)

    expected = {}
    for i in range(n_docs):
        scores = []
        for j in range(n_docs):
            if i == j: continue
            scores.append((j, cosine_sim(tfidf_matrix[i], tfidf_matrix[j])))
        # Sort descending by score. In case of tie, Rust's sort_by with partial_cmp keeps original order (stable sort in Rust? No, sort_by is stable, but wait, the prompt says scores.sort_by which is stable since Rust 1.0).
        # We will just round to 5 decimals to avoid float precision issues and rely on stable sort.
        scores.sort(key=lambda x: round(x[1], 5), reverse=True)
        expected[docs[i][0]] = [docs[scores[0][0]][0], docs[scores[1][0]][0]]

    return expected

def test_recommendations_csv_exists_and_correct():
    csv_path = "/home/user/recommendations.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist. Did the program run successfully?"

    expected = compute_expected_recommendations()

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 5, f"Expected 5 rows in {csv_path}, found {len(rows)}"

    actual = {}
    for row in rows:
        assert len(row) == 3, f"Expected 3 columns per row, found {len(row)} in row: {row}"
        actual[row[0]] = [row[1], row[2]]

    for doc_id, expected_sims in expected.items():
        assert doc_id in actual, f"Document {doc_id} missing from output."
        # Because of potential floating point differences or tie-breaking order, we check the first recommendation strictly,
        # but if there's a tie, we might need to be lenient. However, for this dataset, the top similarities are quite distinct.
        assert actual[doc_id] == expected_sims, f"For {doc_id}, expected similar docs {expected_sims}, but got {actual[doc_id]}"

def test_rust_code_fixed():
    main_rs_path = "/home/user/paper_recommender/src/main.rs"
    assert os.path.isfile(main_rs_path), "main.rs is missing."

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Verify the buggy integer division is gone
    assert "let tf = (count / total_terms) as f64;" not in content, "The intentional bug (integer division) is still present in main.rs"

    # Check that some form of float division is used
    assert "as f64" in content, "The fix should cast count and total_terms to f64 for proper division."