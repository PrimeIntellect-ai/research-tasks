# test_final_state.py
import os
import subprocess
import pytest

def test_cleaner_c_exists():
    assert os.path.isfile("/home/user/cleaner.c"), "/home/user/cleaner.c does not exist"

def test_test_pipeline_sh_exists_and_executable():
    script_path = "/home/user/test_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_pipeline_execution():
    script_path = "/home/user/test_pipeline.sh"
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_pipeline.sh failed with exit code {result.returncode}. stderr: {result.stderr}"
    assert "PASS: Reproducible" in result.stdout, f"test_pipeline.sh did not print 'PASS: Reproducible'. stdout: {result.stdout}"

def test_clean_embeddings_output():
    orig_path = "/home/user/data/embeddings.csv"
    clean_path = "/home/user/clean_embeddings.csv"

    assert os.path.isfile(orig_path), f"Original data {orig_path} missing"
    assert os.path.isfile(clean_path), f"Cleaned data {clean_path} missing"

    with open(orig_path, 'r') as f:
        orig_lines = [line.strip() for line in f if line.strip()]

    with open(clean_path, 'r') as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    assert len(clean_lines) == 50, f"Expected 50 rows in cleaned data, got {len(clean_lines)}"

    expected_cols = [0, 1, 2, 4, 5, 6, 8, 9]

    for i, (orig_line, clean_line) in enumerate(zip(orig_lines, clean_lines)):
        orig_vals = [float(x) for x in orig_line.split(',')]
        clean_vals = [float(x) for x in clean_line.split(',')]

        assert len(clean_vals) == 8, f"Row {i} in cleaned data does not have exactly 8 columns"

        for new_idx, old_idx in enumerate(expected_cols):
            diff = abs(clean_vals[new_idx] - orig_vals[old_idx])
            assert diff < 1e-5, f"Value mismatch in row {i}, new col {new_idx} (old col {old_idx}). Expected ~{orig_vals[old_idx]}, got {clean_vals[new_idx]}"