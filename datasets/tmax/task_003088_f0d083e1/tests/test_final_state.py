# test_final_state.py
import os

def test_go_program_exists():
    """Test that the Go program exists."""
    go_path = "/home/user/bayes_check.go"
    assert os.path.exists(go_path), f"Required file is missing: {go_path}"
    assert os.path.isfile(go_path), f"Path is not a file: {go_path}"

def test_bash_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Required file is missing: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"File is not executable: {script_path}"

def test_results_files():
    """Test that results.txt and results2.txt exist and have the correct contents."""
    results1_path = "/home/user/results.txt"
    results2_path = "/home/user/results2.txt"

    assert os.path.exists(results1_path), f"Required file is missing: {results1_path}"
    assert os.path.exists(results2_path), f"Required file is missing: {results2_path}"

    expected_lines = [
        "ds_001,0.987097",
        "ds_002,0.095238",
        "ds_003,0.999898"
    ]

    with open(results1_path, "r") as f:
        content1 = f.read().strip().splitlines()

    with open(results2_path, "r") as f:
        content2 = f.read().strip().splitlines()

    assert content1 == expected_lines, f"Incorrect contents in {results1_path}"
    assert content2 == expected_lines, f"Incorrect contents in {results2_path}"

def test_pipeline_log():
    """Test that pipeline.log exists and contains the correct outputs."""
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Required file is missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Reproducible: YES" in content, f"'Reproducible: YES' not found in {log_path}"
    assert "Sum: 2.082233" in content, f"'Sum: 2.082233' not found in {log_path}"