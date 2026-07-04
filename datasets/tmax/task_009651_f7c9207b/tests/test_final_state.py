# test_final_state.py
import os
import subprocess
import pytest

def test_bench_results_exists():
    path = "/home/user/api-gateway/bench_results.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the benchmark and save the output?"

def test_bench_results_content():
    path = "/home/user/api-gateway/bench_results.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "BenchmarkSanitize" in content, f"File {path} does not contain 'BenchmarkSanitize'. Ensure you ran the benchmark correctly."

def test_go_tests_pass():
    cwd = "/home/user/api-gateway"
    assert os.path.isdir(cwd), f"Directory {cwd} does not exist."

    try:
        result = subprocess.run(
            ["go", "test"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
    except FileNotFoundError:
        pytest.fail("The 'go' command was not found. Is Go installed?")
    except subprocess.TimeoutExpired:
        pytest.fail("The 'go test' command timed out. There might be a deadlock or an infinite loop.")

    assert result.returncode == 0, f"'go test' failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"