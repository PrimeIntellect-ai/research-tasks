# test_final_state.py

import os

def test_run_search_script_exists_and_executable():
    """Test that the run_search.sh script exists and is executable."""
    script_path = "/home/user/run_search.sh"
    assert os.path.isfile(script_path), f"Missing required script file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script file {script_path} is not executable."

def test_stable_k_file():
    """Test that stable_k.txt exists and contains the correct value."""
    result_path = "/home/user/stable_k.txt"
    assert os.path.isfile(result_path), f"Missing result file: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "0.17", f"Expected stable_k.txt to contain '0.17', but found '{content}'."

def test_output_notebook_exists():
    """Test that the output notebook was generated."""
    output_path = "/home/user/output.ipynb"
    assert os.path.isfile(output_path), f"Missing output notebook file: {output_path}"