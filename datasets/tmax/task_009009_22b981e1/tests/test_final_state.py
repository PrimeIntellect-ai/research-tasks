# test_final_state.py
import os
import math
import pytest

def test_top_pair_txt_exists_and_correct():
    csv_path = "/home/user/project/embeddings.csv"
    out_path = "/home/user/project/top_pair.txt"

    assert os.path.isfile(csv_path), f"The file {csv_path} is missing."
    assert os.path.isfile(out_path), f"The file {out_path} is missing. Did you run the compiled C program?"

    # Read the embeddings and recompute the expected result
    vecs = []
    with open(csv_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                vecs.append([float(x) for x in line.split(",")])

    assert len(vecs) > 1, "Not enough vectors in embeddings.csv to compute correlation."

    max_corr = -2.0
    best_i = -1
    best_j = -1

    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            v1 = vecs[i]
            v2 = vecs[j]

            mean1 = sum(v1) / len(v1)
            mean2 = sum(v2) / len(v2)

            cov = sum((x - mean1) * (y - mean2) for x, y in zip(v1, v2))
            var1 = sum((x - mean1)**2 for x in v1)
            var2 = sum((y - mean2)**2 for y in v2)

            if var1 * var2 == 0:
                corr = 0.0
            else:
                corr = cov / math.sqrt(var1 * var2)

            if corr > max_corr:
                max_corr = corr
                best_i = i
                best_j = j

    expected_output = f"{best_i},{best_j},{max_corr:.4f}"

    with open(out_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Incorrect output in top_pair.txt. "
        f"Expected '{expected_output}', but found '{actual_output}'."
    )

def test_c_code_fixed():
    c_path = "/home/user/project/compute_correlation.c"
    assert os.path.isfile(c_path), f"The file {c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    # The original buggy code used integer arithmetic for sum_i and sum_j
    assert "int sum_i = 0, sum_j = 0;" not in content, (
        "The C code still contains the integer arithmetic bug for sum_i and sum_j. "
        "These should be floats to prevent truncation."
    )