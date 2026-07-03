# test_final_state.py
import os

def test_run_experiment_script_exists_and_executable():
    """Test that the run_experiment.sh script exists and is executable."""
    script_path = "/home/user/run_experiment.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_experiment_log_exists():
    """Test that the experiment_log.txt file exists."""
    log_path = "/home/user/experiment_log.txt"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

def test_experiment_log_content():
    """Test that the experiment_log.txt contains the correct results."""
    log_path = "/home/user/experiment_log.txt"
    if not os.path.isfile(log_path):
        return # Handled by previous test

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "invalid_chars.csv:INVALID_SCHEMA",
        "invalid_cols.csv:INVALID_SCHEMA",
        "invalid_floats.csv:INVALID_SCHEMA",
        "valid_1.csv:-16",
        "valid_na.csv:36"
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, (
        f"The content of {log_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )