# test_final_state.py

import os
import subprocess
import pytest

def test_libhwscore_so_exists():
    path = "/home/user/clib/libhwscore.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist. Did you fix the Makefile and run make?"

    # Check if it's actually an ELF shared object
    try:
        output = subprocess.check_output(["file", path], text=True)
        assert "shared object" in output, f"{path} is not a valid shared object."
    except FileNotFoundError:
        pass # If 'file' command is not available, skip this check

def test_pipeline_go_exists():
    path = "/home/user/pipeline.go"
    assert os.path.isfile(path), f"Go source file {path} does not exist."

def test_pipeline_test_go_exists():
    path = "/home/user/pipeline_test.go"
    assert os.path.isfile(path), f"Go test file {path} does not exist."

def test_eval_results_correct():
    path = "/home/user/eval_results.txt"
    assert os.path.isfile(path), f"Results file {path} does not exist. Did you run your Go program?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["1024", "122", "227", "90"]
    assert lines == expected, f"Contents of {path} do not match the expected results. Got {lines}, expected {expected}."

def test_go_test_passes():
    # Run go test pipeline_test.go pipeline.go
    try:
        result = subprocess.run(
            ["go", "test", "pipeline_test.go", "pipeline.go"],
            cwd="/home/user",
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Go tests failed or did not compile:\n{result.stdout}\n{result.stderr}"
    except FileNotFoundError:
        pytest.fail("Go toolchain not found.")