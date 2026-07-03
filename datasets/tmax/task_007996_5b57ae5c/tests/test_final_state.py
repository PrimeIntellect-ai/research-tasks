# test_final_state.py

import os
import subprocess
import pytest

def test_c_source_exists():
    assert os.path.isfile("/home/user/graph_projector.c"), "C source file /home/user/graph_projector.c not found."

def test_executable_exists_and_runs():
    exe_path = "/home/user/graph_projector"
    assert os.path.isfile(exe_path), f"Executable {exe_path} not found. Did you compile the C program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    csv_path = "/home/user/top_connections.csv"
    if os.path.exists(csv_path):
        os.remove(csv_path)

    try:
        result = subprocess.run([exe_path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Executable failed with return code {result.returncode}.\nStderr: {result.stderr}\nStdout: {result.stdout}"
    except subprocess.TimeoutExpired:
        pytest.fail("Executable timed out after 10 seconds.")

def test_csv_output_correct():
    csv_path = "/home/user/top_connections.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} was not created by the executable."

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected = (
        "Engineering,Marketing,250\n"
        "HR,Engineering,400\n"
        "Marketing,HR,300\n"
        "Sales,Marketing,600"
    )

    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected.splitlines() if line.strip()]

    assert content_lines == expected_lines, f"CSV output did not match expected.\nGot:\n{content}\n\nExpected:\n{expected}"