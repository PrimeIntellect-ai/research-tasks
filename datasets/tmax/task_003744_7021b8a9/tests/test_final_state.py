# test_final_state.py

import os
import csv
import json
import math
import pytest
import requests

def get_true_similarities(query_id):
    data_path = "/home/user/data/artifacts.csv"
    if not os.path.exists(data_path):
        pytest.fail(f"Data file is missing at {data_path}")

    artifacts = {}
    with open(data_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            art_id = row['artifact_id']
            vec = [float(row[f'f{i}']) for i in range(1, 6)]
            artifacts[art_id] = vec

    if query_id not in artifacts:
        pytest.fail(f"Query ID {query_id} not found in artifacts.csv")

    q_vec = artifacts[query_id]
    q_norm = math.sqrt(sum(x*x for x in q_vec))

    similarities = []
    for art_id, vec in artifacts.items():
        if art_id == query_id:
            continue
        dot = sum(x*y for x, y in zip(q_vec, vec))
        norm = math.sqrt(sum(x*x for x in vec))
        sim = dot / (q_norm * norm)
        similarities.append((art_id, sim))

    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in similarities[:3]]

def test_plot_exists():
    plot_path = "/home/user/artifact_clusters.png"
    assert os.path.isfile(plot_path), f"Plot file is missing at {plot_path}"
    assert os.path.getsize(plot_path) > 0, "Plot file is empty"

def test_vendored_package_math_ops_fixed():
    math_ops_path = "/app/mlops-artifact-utils/mlops_artifact_utils/math_ops.py"
    assert os.path.isfile(math_ops_path), f"math_ops.py missing at {math_ops_path}"

    with open(math_ops_path, "r") as f:
        content = f.read()
        assert "norms[:, np.newaxis] * norms[np.newaxis, :]" in content or \
               "*" in content and "+" not in content.split("return")[-1], \
               "Bug in math_ops.py (division by sum of norms) was not fixed correctly"

def test_vendored_package_plot_ops_fixed():
    plot_ops_path = "/app/mlops-artifact-utils/mlops_artifact_utils/plot_ops.py"
    assert os.path.isfile(plot_ops_path), f"plot_ops.py missing at {plot_ops_path}"

    with open(plot_ops_path, "r") as f:
        content = f.read()
        assert "matplotlib.use('Agg')" in content or "matplotlib.use(\"Agg\")" in content, \
               "TkAgg backend setting in plot_ops.py was not changed to Agg"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/api/v1/similar?id=art_1"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth, got {response.status_code}"

def test_api_wrong_auth():
    url = "http://127.0.0.1:8080/api/v1/similar?id=art_1"
    headers = {"Authorization": "Bearer wrong-secret"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong auth, got {response.status_code}"

def test_api_authorized_and_correct():
    url = "http://127.0.0.1:8080/api/v1/similar?id=art_1"
    headers = {"Authorization": "Bearer mlops-secret-77"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "query_id" in data, "Response JSON missing 'query_id'"
    assert "top_3_similar" in data, "Response JSON missing 'top_3_similar'"

    assert data["query_id"] == "art_1", f"Expected query_id 'art_1', got {data['query_id']}"

    expected_top_3 = get_true_similarities("art_1")
    actual_top_3 = data["top_3_similar"]

    assert isinstance(actual_top_3, list), "top_3_similar must be a list"
    assert len(actual_top_3) == 3, f"Expected exactly 3 similar artifacts, got {len(actual_top_3)}"

    assert actual_top_3 == expected_top_3, f"Expected top 3 similar artifacts to be {expected_top_3}, got {actual_top_3}"