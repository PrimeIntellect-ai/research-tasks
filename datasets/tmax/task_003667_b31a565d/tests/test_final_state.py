# test_final_state.py

import os
import json
import pytest

def test_virtual_environment_exists():
    """Test that the virtual environment was created at /home/user/bioenv."""
    venv_dir = "/home/user/bioenv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."

    # Check for python executable in the venv
    python_bin = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found at {python_bin}. Is it a valid virtual environment?"

def test_notebooks_exist():
    """Test that both the original and executed notebooks exist."""
    orig_notebook = "/home/user/sequence_analysis.ipynb"
    exec_notebook = "/home/user/sequence_analysis_executed.ipynb"

    assert os.path.isfile(orig_notebook), f"Original notebook {orig_notebook} does not exist."
    assert os.path.isfile(exec_notebook), f"Executed notebook {exec_notebook} does not exist."

    # Check that they are valid JSON (Jupyter notebooks are JSON)
    for nb in [orig_notebook, exec_notebook]:
        with open(nb, "r") as f:
            try:
                json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"Notebook {nb} is not a valid JSON file.")

def test_results_json_exists_and_correct():
    """Test that results.json exists and contains the correct output."""
    results_file = "/home/user/results.json"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not a valid JSON file.")

    expected_keys = {"best_seq_id", "forward_primer", "reverse_primer", "stability_passed"}
    assert set(results.keys()) == expected_keys, f"Keys in results.json do not match expected keys. Found: {list(results.keys())}"

    assert results["best_seq_id"] == "seq_02_coding", f"Expected best_seq_id to be 'seq_02_coding', got {results['best_seq_id']}"
    assert results["forward_primer"] == "ATGATGATGATGATGATGAT", f"Expected forward_primer to be 'ATGATGATGATGATGATGAT', got {results['forward_primer']}"
    assert results["reverse_primer"] == "CATCATCATCATCATCATCA", f"Expected reverse_primer to be 'CATCATCATCATCATCATCA', got {results['reverse_primer']}"
    assert results["stability_passed"] is True, f"Expected stability_passed to be True, got {results['stability_passed']}"