# test_final_state.py

import os
import struct
import math
import pytest

def read_vectors(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    num_floats = len(data) // 4
    floats = struct.unpack(f'<{num_floats}f', data)
    vectors = []
    for i in range(100):
        vectors.append(list(floats[i*64:(i+1)*64]))
    return vectors

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def norm(v):
    return math.sqrt(sum(x * x for x in v))

def cos_sim(v1, v2):
    n1 = norm(v1)
    n2 = norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot(v1, v2) / (n1 * n2)

def compute_ground_truth():
    vectors = read_vectors('/home/user/embeddings.bin')

    # Exact similarities
    exact_sims = []
    for i in range(1, 100):
        exact_sims.append(cos_sim(vectors[0], vectors[i]))

    # Top 3 indices
    indexed_sims = list(enumerate(exact_sims, start=1))
    indexed_sims.sort(key=lambda x: x[1], reverse=True)
    top3 = [x[0] for x in indexed_sims[:3]]

    # Quantized vectors
    q_vectors = []
    for v in vectors:
        q_vectors.append([round(x * 127.0) / 127.0 for x in v])

    # Quantized similarities
    q_sims = []
    for i in range(1, 100):
        q_sims.append(cos_sim(q_vectors[0], q_vectors[i]))

    # Errors
    errors = [e - q for e, q in zip(exact_sims, q_sims)]

    # Stats
    mean_err = sum(errors) / len(errors)
    variance = sum((e - mean_err)**2 for e in errors) / (len(errors) - 1)
    std_err = math.sqrt(variance)
    ci_margin = 1.96 * std_err / math.sqrt(99)

    return top3, mean_err, ci_margin

def test_results_file():
    results_path = '/home/user/results.txt'
    assert os.path.isfile(results_path), f"File {results_path} is missing."

    with open(results_path, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    assert len(lines) >= 3, "Results file must contain at least 3 lines."

    top3, mean_err, ci_margin = compute_ground_truth()

    expected_top3 = f"Top3_Indices: {top3[0]}, {top3[1]}, {top3[2]}"
    assert lines[0] == expected_top3, f"Expected '{expected_top3}', got '{lines[0]}'"

    try:
        agent_mean = float(lines[1].split(": ")[1])
    except Exception:
        pytest.fail(f"Could not parse Mean_Error from line: {lines[1]}")

    assert abs(agent_mean - mean_err) < 1e-5, f"Mean error mismatch. Expected around {mean_err:.6f}, got {agent_mean}"

    try:
        agent_ci = float(lines[2].split(": ")[1])
    except Exception:
        pytest.fail(f"Could not parse CI_Margin from line: {lines[2]}")

    assert abs(agent_ci - ci_margin) < 1e-5, f"CI margin mismatch. Expected around {ci_margin:.6f}, got {agent_ci}"