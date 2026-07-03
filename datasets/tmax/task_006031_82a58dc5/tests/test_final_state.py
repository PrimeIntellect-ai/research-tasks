# test_final_state.py

import os
import re
import pytest

def test_source_code_exists():
    assert os.path.exists("/home/user/mcmc_graph.c"), "The C source file /home/user/mcmc_graph.c is missing."
    assert os.path.isfile("/home/user/mcmc_graph.c"), "/home/user/mcmc_graph.c is not a file."

def test_compiled_binary_exists():
    binary_path = "/home/user/mcmc_graph"
    assert os.path.exists(binary_path), f"The compiled binary {binary_path} is missing."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_results_file_correctness():
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"The results file {results_path} is missing."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {results_path}, but found {len(lines)}."

    # Check Analytical result
    analytical_match = re.match(r"^Analytical:\s*([0-9]+\.[0-9]+)$", lines[0])
    assert analytical_match, f"First line '{lines[0]}' does not match the expected format 'Analytical: 0.XXXX'."

    analytical_val = float(analytical_match.group(1))
    assert abs(analytical_val - 0.2000) < 1e-5, f"Expected Analytical value to be 0.2000, got {analytical_val:.4f}."

    # Check MCMC result
    mcmc_match = re.match(r"^MCMC:\s*([0-9]+\.[0-9]+)$", lines[1])
    assert mcmc_match, f"Second line '{lines[1]}' does not match the expected format 'MCMC: 0.XXXX'."

    mcmc_val = float(mcmc_match.group(1))
    assert 0.1900 <= mcmc_val <= 0.2100, f"Expected MCMC value to be close to 0.2000 (between 0.1900 and 0.2100), got {mcmc_val:.4f}."