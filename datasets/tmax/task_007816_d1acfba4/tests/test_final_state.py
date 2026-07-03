# test_final_state.py

import os
import pytest

def test_pipeline_script_exists():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} is missing."

def test_results_tsv_content():
    results_path = "/home/user/results.tsv"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    expected_lines = [
        "mol_A\t4\t1600\t80.1",
        "mol_C\t4\t1950\t95.5"
    ]

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {results_path}, but found {len(lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, lines)):
        expected_parts = expected.split("\t")
        actual_parts = actual.split("\t")

        assert len(actual_parts) == 4, f"Line {i+1} does not have exactly 4 tab-separated columns."
        assert actual_parts[0] == expected_parts[0], f"Line {i+1} molecule name mismatch: expected {expected_parts[0]}, got {actual_parts[0]}."
        assert actual_parts[1] == expected_parts[1], f"Line {i+1} max degree mismatch: expected {expected_parts[1]}, got {actual_parts[1]}."
        assert actual_parts[2] == expected_parts[2], f"Line {i+1} peak frequency mismatch: expected {expected_parts[2]}, got {actual_parts[2]}."

        # Float comparison for intensity
        try:
            actual_intensity = float(actual_parts[3])
            expected_intensity = float(expected_parts[3])
            assert abs(actual_intensity - expected_intensity) < 1e-6, f"Line {i+1} peak intensity mismatch: expected {expected_intensity}, got {actual_intensity}."
        except ValueError:
            pytest.fail(f"Line {i+1} peak intensity is not a valid float: {actual_parts[3]}")