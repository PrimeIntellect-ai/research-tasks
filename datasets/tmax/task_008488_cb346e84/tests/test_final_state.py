# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

DEPS_PATH = "/home/user/deps.json"
CALCULATE_SCRIPT = "/home/user/calculate.sh"
WEIGHTS_JSON = "/home/user/weights.json"
ARTIFACT_S = "/home/user/artifact.s"
ARTIFACT_BIN = "/home/user/artifact"

def compute_expected_weights(deps_path):
    with open(deps_path, 'r') as f:
        data = json.load(f)

    nodes = data['nodes']
    edges = data['edges']

    out_degree = {n: 0 for n in nodes}
    in_edges = {n: [] for n in nodes}

    for e in edges:
        u = e['from']
        v = e['to']
        out_degree[u] += 1
        in_edges[v].append(u)

    weights = {n: 100 for n in nodes}

    for _ in range(3):
        new_weights = {}
        for n in nodes:
            w = 100
            for m in in_edges[n]:
                if out_degree[m] > 0:
                    w += weights[m] // out_degree[m]
            new_weights[n] = w
        weights = new_weights

    return weights

def test_calculate_script_exists():
    assert os.path.exists(CALCULATE_SCRIPT), f"Missing script: {CALCULATE_SCRIPT}"
    assert os.path.isfile(CALCULATE_SCRIPT), f"Not a file: {CALCULATE_SCRIPT}"

def test_weights_json_correct():
    assert os.path.exists(WEIGHTS_JSON), f"Missing weights file: {WEIGHTS_JSON}"

    with open(WEIGHTS_JSON, 'r') as f:
        try:
            student_weights = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {WEIGHTS_JSON} is not valid JSON")

    expected_weights = compute_expected_weights(DEPS_PATH)

    # Convert expected keys to string for JSON comparison
    expected_weights_str = {str(k): v for k, v in expected_weights.items()}

    assert student_weights == expected_weights_str, f"Weights do not match expected values. Expected: {expected_weights_str}, Got: {student_weights}"

def test_artifact_source_exists():
    assert os.path.exists(ARTIFACT_S), f"Missing assembly file: {ARTIFACT_S}"
    assert os.path.isfile(ARTIFACT_S), f"Not a file: {ARTIFACT_S}"

def test_artifact_executable_exists_and_runs():
    assert os.path.exists(ARTIFACT_BIN), f"Missing executable: {ARTIFACT_BIN}"
    assert os.path.isfile(ARTIFACT_BIN), f"Not a file: {ARTIFACT_BIN}"

    st = os.stat(ARTIFACT_BIN)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {ARTIFACT_BIN} is not executable"

    expected_weights = compute_expected_weights(DEPS_PATH)

    # Find winning node: highest weight, tie-break lowest ID
    max_weight = -1
    winning_node = -1
    for node, weight in expected_weights.items():
        if weight > max_weight:
            max_weight = weight
            winning_node = node
        elif weight == max_weight:
            if node < winning_node:
                winning_node = node

    # Run the artifact and check exit code
    result = subprocess.run([ARTIFACT_BIN])
    assert result.returncode == winning_node, f"Expected exit code {winning_node}, but got {result.returncode}"