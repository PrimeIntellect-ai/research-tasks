# test_final_state.py

import os
import math
from collections import Counter
import pytest

def compute_expected_result(corpus_path):
    with open(corpus_path, "r") as f:
        docs = [line.strip().lower().split() for line in f if line.strip()]

    tfs = []
    for doc in docs:
        counts = Counter(doc)
        total = len(doc)
        tfs.append({k: v / total for k, v in counts.items()})

    max_sim = -1.0
    best_i, best_j = -1, -1

    for i in range(len(tfs)):
        for j in range(i + 1, len(tfs)):
            dot = sum(tfs[i].get(k, 0) * tfs[j].get(k, 0) for k in set(tfs[i]) | set(tfs[j]))
            norm_a = sum(v * v for v in tfs[i].values())
            norm_b = sum(v * v for v in tfs[j].values())

            if norm_a == 0 or norm_b == 0:
                sim = 0.0
            else:
                sim = dot / (math.sqrt(norm_a) * math.sqrt(norm_b))

            # Match the Go script logic: strict greater than
            if sim > max_sim:
                max_sim = sim
                best_i = i
                best_j = j

    return f"{best_i},{best_j},{max_sim:.4f}"

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    corpus_path = "/home/user/corpus.txt"

    assert os.path.exists(corpus_path), f"Corpus file missing at {corpus_path}"
    assert os.path.exists(result_path), f"Result file missing at {result_path}. The Go script might not have been executed successfully."

    expected_content = compute_expected_result(corpus_path)

    with open(result_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Result file content is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{actual_content}'\n"
        f"Check if the integer division bug was properly fixed and the script was recompiled/run."
    )