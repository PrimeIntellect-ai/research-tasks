# test_final_state.py
import os
import json
import csv
import math
import pytest

RESULTS_PATH = "/home/user/results.json"
VECTORS_PATH = "/home/user/vectors.csv"
QUERIES_PATH = "/home/user/queries.csv"

def compute_pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
    var_x = sum((a - mean_x) ** 2 for a in x)
    var_y = sum((b - mean_y) ** 2 for b in y)

    if var_x == 0 or var_y == 0:
        return 0.0
    return cov / math.sqrt(var_x * var_y)

def compute_cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a ** 2 for a in vec1))
    norm_b = math.sqrt(sum(b ** 2 for b in vec2))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

@pytest.fixture(scope="module")
def expected_data():
    # Read vectors
    vectors = []
    f1_vals = []
    f2_vals = []

    with open(VECTORS_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            doc_id = row[0]
            features = [float(val) for val in row[1:]]
            vectors.append((doc_id, features))
            f1_vals.append(features[0])
            f2_vals.append(features[1])

    # Read queries
    query_1_features = None
    with open(QUERIES_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == "Query_1":
                query_1_features = [float(val) for val in row[1:]]
                break

    assert query_1_features is not None, "Query_1 not found in queries.csv"

    # Compute expected correlation
    expected_corr = compute_pearson_correlation(f1_vals, f2_vals)

    # Compute expected top 3
    similarities = []
    for doc_id, features in vectors:
        sim = compute_cosine_similarity(query_1_features, features)
        similarities.append((doc_id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    expected_top_3 = [x[0] for x in similarities[:3]]

    return {
        "correlation": expected_corr,
        "top_3": expected_top_3
    }

@pytest.fixture
def results_data():
    assert os.path.exists(RESULTS_PATH), f"Missing results file: {RESULTS_PATH}"
    with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON")
    return data

def test_results_format(results_data):
    """Test that results.json contains the expected keys."""
    expected_keys = {"correlation_F1_F2", "query_1_top_3", "benchmark_avg_ms"}
    missing_keys = expected_keys - set(results_data.keys())
    assert not missing_keys, f"results.json is missing keys: {missing_keys}"

def test_correlation_value(results_data, expected_data):
    """Test that the computed correlation is correct."""
    actual_corr = results_data.get("correlation_F1_F2")
    assert isinstance(actual_corr, (int, float)), "correlation_F1_F2 must be a number"

    expected_corr = expected_data["correlation"]
    # Check within 0.002 tolerance as per truth logic
    assert math.isclose(actual_corr, expected_corr, abs_tol=0.002), \
        f"Correlation mismatch. Expected ~{expected_corr:.3f}, got {actual_corr}"

def test_top_3_results(results_data, expected_data):
    """Test that the top 3 similar documents are correct."""
    actual_top_3 = results_data.get("query_1_top_3")
    assert isinstance(actual_top_3, list), "query_1_top_3 must be a list"
    assert len(actual_top_3) == 3, "query_1_top_3 must contain exactly 3 elements"

    expected_top_3 = expected_data["top_3"]
    assert actual_top_3 == expected_top_3, \
        f"Top 3 mismatch. Expected {expected_top_3}, got {actual_top_3}"

def test_benchmark_value(results_data):
    """Test that the benchmark value is a positive number."""
    benchmark_ms = results_data.get("benchmark_avg_ms")
    assert isinstance(benchmark_ms, (int, float)), "benchmark_avg_ms must be a number"
    assert benchmark_ms > 0, f"benchmark_avg_ms must be greater than 0, got {benchmark_ms}"