# test_final_state.py

import os
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_script():
    script_path = "/home/user/investigate_leak.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the student's script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute successfully. Stderr:\n{result.stderr}"

def test_leaked_ids():
    path = "/home/user/leaked_ids.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["102", "108"]
    assert lines == expected, f"Incorrect contents in {path}. Expected {expected}, got {lines}"

def test_leaked_features():
    path = "/home/user/leaked_features.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["102,0.6,60", "108,0.4,40"]
    assert lines == expected, f"Incorrect contents in {path}. Expected {expected}, got {lines}"

def test_leak_predictions():
    path = "/home/user/leak_predictions.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["Prediction for 102: 0.99", "Prediction for 108: 0.99"]
    assert lines == expected, f"Incorrect contents in {path}. Expected {expected}, got {lines}"

def test_benchmark_output():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "real " in content, f"'real' timing not found in {path}"
    assert "user " in content, f"'user' timing not found in {path}"
    assert "sys " in content, f"'sys' timing not found in {path}"