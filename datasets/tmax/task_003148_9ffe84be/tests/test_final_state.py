# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_run_experiment_exists_and_executable():
    path = "/home/user/run_experiment.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"{path} is not executable."

def test_search_py_exists():
    path = "/home/user/search.py"
    assert os.path.isfile(path), f"{path} does not exist."

def test_metrics_json_validity_and_contents():
    path = "/home/user/metrics.json"
    assert os.path.isfile(path), f"{path} does not exist. Did run_experiment.sh run successfully?"

    with open(path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    required_keys = ["max_abs_error", "naive_time_sec", "optimized_time_sec", "speedup", "top_5_indices"]
    for key in required_keys:
        assert key in metrics, f"Key '{key}' is missing from metrics.json."

    assert isinstance(metrics["max_abs_error"], (int, float)), "max_abs_error must be a float."
    assert metrics["max_abs_error"] < 1e-4, f"max_abs_error {metrics['max_abs_error']} is not < 1e-4."

    assert isinstance(metrics["naive_time_sec"], (int, float)), "naive_time_sec must be a float."
    assert isinstance(metrics["optimized_time_sec"], (int, float)), "optimized_time_sec must be a float."
    assert isinstance(metrics["speedup"], (int, float)), "speedup must be a float."

    assert metrics["speedup"] > 1.0, f"speedup {metrics['speedup']} is not > 1.0. Optimized search should be faster."

    assert isinstance(metrics["top_5_indices"], list), "top_5_indices must be a list."
    assert len(metrics["top_5_indices"]) == 100, f"Expected 100 queries in top_5_indices, got {len(metrics['top_5_indices'])}."

    # We use a subprocess to compute the expected indices with numpy/h5py, 
    # to strictly keep this test file using only the standard library.
    verify_script = """
import h5py
import numpy as np
import json

docs = []
for i in range(5):
    with h5py.File(f"/home/user/data/docs_{i}.h5", "r") as f:
        docs.append(f["embeddings"][:])
docs = np.vstack(docs)

with h5py.File("/home/user/queries.h5", "r") as f:
    queries = f["queries"][:]

docs_norm = docs / np.linalg.norm(docs, axis=1, keepdims=True)
queries_norm = queries / np.linalg.norm(queries, axis=1, keepdims=True)
sim = queries_norm @ docs_norm.T

expected_top_5 = np.argsort(-sim, axis=1)[:, :5].tolist()
print(json.dumps(expected_top_5))
"""
    result = subprocess.run(["python3", "-c", verify_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute expected indices: {result.stderr}"

    expected_top_5 = json.loads(result.stdout)
    assert metrics["top_5_indices"] == expected_top_5, "top_5_indices do not match the expected canonical values."