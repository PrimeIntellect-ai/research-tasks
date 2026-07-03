# test_final_state.py
import json
import os
import numpy as np
import redis
from scipy.stats import wasserstein_distance
import pytest

def test_processed_graph_exists_and_valid():
    output_path = '/home/user/processed_graph.json'
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON.")

    assert 'wasserstein_distance' in data, "Key 'wasserstein_distance' missing in output."
    assert 'edges' in data, "Key 'edges' missing in output."

    agent_wd = data['wasserstein_distance']
    assert isinstance(agent_wd, (int, float)), "'wasserstein_distance' must be a number."

def test_wasserstein_distance_metric():
    output_path = '/home/user/processed_graph.json'
    if not os.path.exists(output_path):
        pytest.fail(f"Output file {output_path} does not exist.")

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON.")

    agent_wd = data.get('wasserstein_distance')
    if agent_wd is None:
        pytest.fail("Key 'wasserstein_distance' missing in output.")

    # Connect to Redis
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        raw_items = r.lrange('raw_traffic', 0, -1)
    except Exception as e:
        pytest.fail(f"Could not connect to Redis or read 'raw_traffic': {e}")

    assert len(raw_items) > 0, "No data found in Redis list 'raw_traffic'."

    # Group by src, dst
    from collections import defaultdict
    edges = defaultdict(list)
    for item_str in raw_items:
        try:
            item = json.loads(item_str)
            src = item['src']
            dst = item['dst']
            latency = item['latency']
            edges[(src, dst)].append(latency)
        except Exception:
            pass

    assert len(edges) > 0, "No valid edge data parsed from Redis."

    # Compute true mean for each edge
    edge_means = []
    for edge, latencies in edges.items():
        edge_means.append(np.mean(latencies))

    # Standardize means
    edge_means = np.array(edge_means)
    mean_of_means = np.mean(edge_means)
    std_of_means = np.std(edge_means, ddof=0)

    if std_of_means > 0:
        standardized_means = (edge_means - mean_of_means) / std_of_means
    else:
        standardized_means = np.zeros_like(edge_means)

    # Compute reference Wasserstein distance
    np.random.seed(42)
    reference_normal = np.random.normal(0, 1, 100000)
    ref_wd = wasserstein_distance(standardized_means, reference_normal)

    error = abs(agent_wd - ref_wd)
    threshold = 0.05

    assert error <= threshold, (
        f"Absolute error of wasserstein_distance {error:.4f} exceeds threshold {threshold}. "
        f"Agent reported: {agent_wd}, Reference computed: {ref_wd:.4f}"
    )