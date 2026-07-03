# test_final_state.py

import os
import stat
import pytest

def test_run_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_tokens_file_created_and_correct():
    tokens_path = "/home/user/data/tokens.txt"
    assert os.path.isfile(tokens_path), f"The tokens file {tokens_path} was not created."

    with open(tokens_path, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    expected_tokens = [
        "hello", "world", "this", "is", "a", "test", "dataset",
        "data", "science", "involves", "linear", "algebra", "tokenization", "and", "environments",
        "testing", "1", "2", "3", "the", "quick", "brown", "fox", "jumps"
    ]

    assert tokens == expected_tokens, f"The tokens in {tokens_path} do not match the expected lowercase, punctuation-free output."

def test_venv_created():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"The virtual environment directory {venv_path} was not created."
    assert os.path.isfile(os.path.join(venv_path, "bin", "python")) or os.path.isfile(os.path.join(venv_path, "bin", "python3")), \
        "The virtual environment does not seem to contain a valid Python executable."

def test_artifacts_generated():
    plot_path = "/home/user/artifacts/plot.png"
    metrics_path = "/home/user/artifacts/eigen_metrics.txt"

    assert os.path.isfile(plot_path), f"The plot artifact {plot_path} was not generated. Ensure the Python script ran successfully with the correct Matplotlib backend."
    assert os.path.isfile(metrics_path), f"The metrics artifact {metrics_path} was not generated. Ensure the Python script ran successfully."

    with open(metrics_path, "r") as f:
        content = f.read()

    assert "Vocab size:" in content, f"The metrics file {metrics_path} does not contain expected content."
    assert "Max Eigenvalue:" in content, f"The metrics file {metrics_path} does not contain expected content."