# test_final_state.py

import os
import pytest

def test_top_sequences_file():
    file_path = "/home/user/top_sequences.txt"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 sequences in {file_path}, but found {len(lines)}."

    expected_seqs = {"SEQ_003", "SEQ_005", "SEQ_001"}
    actual_seqs = set(lines)

    assert actual_seqs == expected_seqs, f"Expected top sequences to be {expected_seqs}, but got {actual_seqs}."

def test_lambda_mean_file():
    file_path = "/home/user/lambda_mean.txt"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    try:
        lambda_mean = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {file_path} as a float. Content: '{content}'")

    # The exponential decay rate for SEQ_003 (which dominates) is ~0.5.
    # We check if the MCMC posterior mean is reasonably close to 0.5.
    assert 0.48 <= lambda_mean <= 0.52, f"Expected lambda mean to be around 0.50, but got {lambda_mean}."

def test_go_module_initialized():
    mod_path = "/home/user/seq_analysis/go.mod"
    assert os.path.exists(mod_path), f"Go module file {mod_path} does not exist."

    with open(mod_path, "r") as f:
        content = f.read()

    assert "gonum.org/v1/gonum" in content, "The gonum package is not listed in go.mod."