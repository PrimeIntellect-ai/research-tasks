# test_final_state.py
import os
import json
import pytest

def test_features_jsonl_exists():
    """Check that the features.jsonl file was generated."""
    path = "/home/user/features.jsonl"
    assert os.path.exists(path), f"Output file missing: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_features_jsonl_contents():
    """Verify the contents and mathematical correctness of features.jsonl."""
    path = "/home/user/features.jsonl"
    assert os.path.exists(path), f"Output file missing: {path}"

    with open(path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) >= 2, f"Expected at least 2 lines in {path}, got {len(lines)}"

    results = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON line: {line}")

        assert "graph_id" in data, f"Missing 'graph_id' in {data}"
        assert "a" in data, f"Missing 'a' in {data}"
        assert "b" in data, f"Missing 'b' in {data}"
        assert "c" in data, f"Missing 'c' in {data}"
        assert "stable" in data, f"Missing 'stable' in {data}"

        results[data["graph_id"]] = data

    # Assert expected logic for graph_0
    assert "graph_0" in results, "Missing results for graph_0"
    g0 = results["graph_0"]
    assert g0["stable"] is True, f"graph_0 should be stable (True), got {g0['stable']}"
    assert abs(g0["a"] - 0.5) < 1e-3, f"graph_0 'a' expected ~0.5, got {g0['a']}"
    assert abs(g0["b"] - (-0.3)) < 1e-3, f"graph_0 'b' expected ~-0.3, got {g0['b']}"
    assert abs(g0["c"] - 0.1) < 1e-3, f"graph_0 'c' expected ~0.1, got {g0['c']}"

    # Assert expected logic for graph_1
    assert "graph_1" in results, "Missing results for graph_1"
    g1 = results["graph_1"]
    assert g1["stable"] is False, f"graph_1 should be unstable (False), got {g1['stable']}"
    assert abs(g1["a"] - 0.0) < 1e-3, f"graph_1 'a' expected ~0.0, got {g1['a']}"
    assert abs(g1["b"] - 3.0) < 1e-3, f"graph_1 'b' expected ~3.0, got {g1['b']}"
    assert abs(g1["c"] - (-3.0)) < 1e-3, f"graph_1 'c' expected ~-3.0, got {g1['c']}"