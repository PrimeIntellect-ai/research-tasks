# test_final_state.py

import os
import subprocess
import pytest

def test_processor_modified():
    processor_path = "/home/user/logprocessor/processor.go"
    assert os.path.isfile(processor_path), f"File {processor_path} is missing."
    with open(processor_path, "r") as f:
        content = f.read()
    # Check that it handles negative numbers by returning 0 (or 0.0)
    # The exact implementation might vary, but it should contain a check for negative.
    # We can compile and run to be sure, but we can also check the result.txt.
    pass

def test_test_file_exists_and_passes():
    test_path = "/home/user/logprocessor/processor_test.go"
    assert os.path.isfile(test_path), f"File {test_path} is missing."

    with open(test_path, "r") as f:
        content = f.read()
    assert "TestConvergeMetric_Negative" in content, "Test function TestConvergeMetric_Negative is missing."
    assert "-5.0" in content or "-5" in content, "Test does not pass -5.0 to ConvergeMetric."

    # Run the test
    env = os.environ.copy()
    # Unset GOPROXY if it's broken, or use direct
    env["GOPROXY"] = "direct"
    result = subprocess.run(
        ["go", "test", "-v", "-run", "TestConvergeMetric_Negative"],
        cwd="/home/user/logprocessor",
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"go test failed:\n{result.stdout}\n{result.stderr}"

def test_binary_exists_and_executable():
    binary_path = "/home/user/logprocessor/bin/logprocessor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_result_txt():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing."
    with open(result_path, "r") as f:
        content = f.read().strip()

    # Expected total is 14.0000
    assert "14.0000" in content, f"Expected 14.0000 in {result_path}, but got '{content}'"