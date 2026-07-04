# test_final_state.py

import os
import json
import math
import pytest

def test_makefile_exists():
    """Test that the Makefile exists in the correct location."""
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "build:" in content, "Makefile is missing the 'build' target."
    assert "run:" in content, "Makefile is missing the 'run' target."
    assert "clean:" in content, "Makefile is missing the 'clean' target."

def test_output_metrics_json():
    """Test that the output_metrics.json file exists and contains the correct computed values."""
    json_path = "/home/user/output_metrics.json"
    assert os.path.isfile(json_path), f"Output file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "unique_points" in data, "JSON is missing the 'unique_points' key."
    assert "centroid" in data, "JSON is missing the 'centroid' key."
    assert "max_distance" in data, "JSON is missing the 'max_distance' key."

    assert data["unique_points"] == 3, f"Expected 3 unique points, got {data['unique_points']}."

    centroid = data["centroid"]
    assert isinstance(centroid, list) and len(centroid) == 3, "Centroid must be a list of 3 floats."

    expected_centroid = [4.0, 5.0, 6.0]
    for i in range(3):
        assert math.isclose(centroid[i], expected_centroid[i], abs_tol=0.01), \
            f"Centroid coordinate {i} expected to be {expected_centroid[i]}, got {centroid[i]}."

    expected_max_distance = 5.20
    assert math.isclose(data["max_distance"], expected_max_distance, abs_tol=0.01), \
        f"Expected max_distance to be {expected_max_distance}, got {data['max_distance']}."