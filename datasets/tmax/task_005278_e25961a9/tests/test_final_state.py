# test_final_state.py
import pytest
import requests

def test_pagerank_service():
    url = "http://127.0.0.1:8080/calculate"
    graph = {"0": ["1", "2"], "1": ["2"], "2": ["0"]}

    try:
        response = requests.post(url, json={"graph": graph}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the PageRank service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "ranks" in data, "Response JSON missing 'ranks' key"
    assert "iterations" in data, "Response JSON missing 'iterations' key"

    ranks = data["ranks"]

    # Compute expected PageRank dynamically using the correct formula
    expected = {node: 1.0 / len(graph) for node in graph}
    damping = 0.85
    N = len(graph)

    for _ in range(1000):
        new_ranks = {}
        diff = 0.0
        for node in graph:
            rank_sum = 0.0
            for in_node, out_edges in graph.items():
                if node in out_edges:
                    rank_sum += expected[in_node] / len(out_edges)
            new_ranks[node] = (1.0 - damping) / N + damping * rank_sum
            diff += abs(new_ranks[node] - expected[node])
        expected = new_ranks
        if diff < 1e-7:
            break

    # Verify the sum of ranks is approximately 1.0
    total_rank = sum(ranks.values())
    assert abs(total_rank - 1.0) < 1e-4, f"Sum of ranks should be ~1.0, got {total_rank}"

    # Verify exact values
    for node, expected_val in expected.items():
        assert node in ranks, f"Node {node} missing from returned ranks"
        actual_val = ranks[node]
        assert abs(actual_val - expected_val) < 1e-4, (
            f"Rank for node {node} is incorrect. "
            f"Expected ~{expected_val:.5f}, got {actual_val:.5f}. "
            "Check damping factor (0.85), tolerance (1e-7), and the math formula."
        )