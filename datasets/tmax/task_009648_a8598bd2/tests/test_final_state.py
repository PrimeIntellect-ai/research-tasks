# test_final_state.py

import os
import subprocess
import pytest

def test_test_features_csv_exists_and_format():
    features_path = "/home/user/test_features.csv"
    assert os.path.exists(features_path), f"Output file is missing: {features_path}"
    assert os.path.isfile(features_path), f"Output path is not a file: {features_path}"

    with open(features_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in test_features.csv, found {len(lines)}"

    # Parse lines into lists of integers
    try:
        line1_tokens = [int(x) for x in lines[0].split(",")]
        line2_tokens = [int(x) for x in lines[1].split(",")]
    except ValueError:
        pytest.fail("test_features.csv contains non-integer values or is not comma-separated.")

    # Check line 1 (urgent your account is locked)
    # "is" was in training set, others were not.
    assert len(line1_tokens) == 5, f"Expected 5 tokens in first test line, got {len(line1_tokens)}"
    assert line1_tokens[0] == 0, "Expected 'urgent' to be UNK (0)"
    assert line1_tokens[1] == 0, "Expected 'your' to be UNK (0)"
    assert line1_tokens[2] == 0, "Expected 'account' to be UNK (0)"
    assert line1_tokens[3] > 0, "Expected 'is' to have a valid vocab ID (>0)"
    assert line1_tokens[4] == 0, "Expected 'locked' to be UNK (0)"

    # Check line 2 (this is a completely unique test message)
    # "is" and "a" were in training set, others were not.
    assert len(line2_tokens) == 7, f"Expected 7 tokens in second test line, got {len(line2_tokens)}"
    assert line2_tokens[0] == 0, "Expected 'this' to be UNK (0)"
    assert line2_tokens[1] > 0, "Expected 'is' to have a valid vocab ID (>0)"
    assert line2_tokens[2] > 0, "Expected 'a' to have a valid vocab ID (>0)"
    assert line2_tokens[3] == 0, "Expected 'completely' to be UNK (0)"
    assert line2_tokens[4] == 0, "Expected 'unique' to be UNK (0)"
    assert line2_tokens[5] == 0, "Expected 'test' to be UNK (0)"
    assert line2_tokens[6] == 0, "Expected 'message' to be UNK (0)"

    # Ensure 'is' has the same ID in both lines
    assert line1_tokens[3] == line2_tokens[1], "Expected 'is' to have the same vocab ID in both test lines"

def test_go_benchmark_file_exists():
    benchmark_path = "/home/user/prepare_data_test.go"
    assert os.path.exists(benchmark_path), f"Benchmark file is missing: {benchmark_path}"
    assert os.path.isfile(benchmark_path), f"Benchmark path is not a file: {benchmark_path}"

    with open(benchmark_path, "r") as f:
        content = f.read()

    assert "BenchmarkTokenize" in content, "BenchmarkTokenize function is missing from prepare_data_test.go"

def test_go_benchmark_runs():
    # Run go test -bench . in /home/user
    try:
        result = subprocess.run(
            ["go", "test", "-bench", "."],
            cwd="/home/user",
            capture_output=True,
            text=True,
            check=True
        )
        assert "BenchmarkTokenize" in result.stdout, "Benchmark did not run or output 'BenchmarkTokenize'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'go test -bench .' failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("The 'go' command was not found. Is Go installed and in PATH?")