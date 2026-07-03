# test_final_state.py

import os
import re
import pytest

def test_cluster_fixed_exists():
    path = "/home/user/clustering/cluster_fixed"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile your fixed code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_final_output_exists():
    path = "/home/user/final_output.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run the final command?"

def test_final_output_content():
    path = "/home/user/final_output.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "NaN" not in content and "nan" not in content, "Output contains NaN. The algorithmic bug (division by zero) might not be fully fixed."

    lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
    assert len(lines) == 3, f"Expected exactly 3 lines of output in {path}, found {len(lines)}."

    centroids = []
    for line in lines:
        match = re.match(r"Centroid \d:\s*([+-]?\d*\.?\d+)", line)
        assert match, f"Line '{line}' does not match expected format 'Centroid X: Y'."
        centroids.append(float(match.group(1)))

    centroids.sort()

    # The points were generated around 10.0, 50.0, and 90.0
    assert 5.0 < centroids[0] < 15.0, f"First centroid {centroids[0]} is not around the expected value of 10.0. Did you fix the partial read bug?"
    assert 45.0 < centroids[1] < 55.0, f"Second centroid {centroids[1]} is not around the expected value of 50.0. Did you fix the partial read bug?"
    assert 85.0 < centroids[2] < 95.0, f"Third centroid {centroids[2]} is not around the expected value of 90.0. Did you fix the partial read bug?"