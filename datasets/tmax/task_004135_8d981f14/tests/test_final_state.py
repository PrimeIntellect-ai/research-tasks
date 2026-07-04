# test_final_state.py
import os
import math
import re

def compute_embeddings(filepath):
    embeddings = []
    with open(filepath, 'r') as f:
        for line in f:
            counts = [0] * 26
            total = 0
            for char in line:
                if char.isalpha():
                    counts[ord(char.lower()) - ord('a')] += 1
                    total += 1
            if total > 0:
                embeddings.append([c / total for c in counts])
            else:
                embeddings.append([0.0] * 26)
    return embeddings

def test_files_exist():
    expected_files = [
        "/home/user/etl/embedder",
        "/home/user/etl/embed_A.csv",
        "/home/user/etl/embed_B.csv",
        "/home/user/etl/evaluate.c",
        "/home/user/etl/metrics.txt"
    ]
    for path in expected_files:
        assert os.path.exists(path), f"Expected file {path} is missing."

def test_metrics_values():
    metrics_path = "/home/user/etl/metrics.txt"
    assert os.path.isfile(metrics_path), f"File {metrics_path} is missing."

    # Recompute ground truth
    embed_A = compute_embeddings("/home/user/etl/dataset_A.txt")
    embed_B = compute_embeddings("/home/user/etl/dataset_B.txt")

    # Centroid A
    N_A = len(embed_A)
    centroid_A = [sum(col) / N_A for col in zip(*embed_A)]

    # Distances for B
    distances = []
    for row in embed_B:
        dist = math.sqrt(sum((a - b)**2 for a, b in zip(row, centroid_A)))
        distances.append(dist)

    N_B = len(distances)
    mean_dist = sum(distances) / N_B
    variance = sum((d - mean_dist)**2 for d in distances) / (N_B - 1) if N_B > 1 else 0
    std_dev = math.sqrt(variance)

    ci_margin = 1.96 * std_dev / math.sqrt(N_B)
    ci_lower = mean_dist - ci_margin
    ci_upper = mean_dist + ci_margin

    expected_metrics = {
        "Centroid_A_Dim0": centroid_A[0],
        "Centroid_A_Dim25": centroid_A[25],
        "Mean_Distance": mean_dist,
        "Std_Dev": std_dev,
        "CI_95_Lower": ci_lower,
        "CI_95_Upper": ci_upper
    }

    # Parse metrics.txt
    parsed_metrics = {}
    with open(metrics_path, 'r') as f:
        for line in f:
            match = re.match(r'^([^:]+):\s*([\d\.\-]+)', line.strip())
            if match:
                key, value = match.groups()
                parsed_metrics[key] = float(value)

    # Validate
    for key, expected_val in expected_metrics.items():
        assert key in parsed_metrics, f"Missing metric {key} in metrics.txt"
        actual_val = parsed_metrics[key]
        assert math.isclose(actual_val, expected_val, abs_tol=1e-4), \
            f"Metric {key} mismatch. Expected ~{expected_val:.6f}, got {actual_val:.6f}"

def test_embed_csv_format():
    embed_a_path = "/home/user/etl/embed_A.csv"
    with open(embed_a_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0, "embed_A.csv is empty."
        for line in lines:
            parts = line.strip().split(',')
            assert len(parts) == 26, f"Expected 26 dimensions in embed_A.csv, got {len(parts)}."
            for p in parts:
                float(p)  # Should not raise ValueError