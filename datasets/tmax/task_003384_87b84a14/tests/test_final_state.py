# test_final_state.py

import os
import subprocess
import pytest

def test_chunker_binary_exists_and_executable():
    binary_path = "/home/user/logchunker/chunker"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_chunker_runs_successfully():
    binary_path = "/home/user/logchunker/chunker"
    # Ensure it runs without panic or exit code != 0
    result = subprocess.run([binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {binary_path} failed with exit code {result.returncode}.\nStderr: {result.stderr}"

def test_go_test_passes():
    test_dir = "/home/user/logchunker"
    result = subprocess.run(["go", "test"], cwd=test_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"'go test' failed in {test_dir}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_main_test_go_contents():
    test_file = "/home/user/logchunker/main_test.go"
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    with open(test_file, 'r') as f:
        content = f.read()

    assert "TestChunkData" in content, "main_test.go does not contain a test function named 'TestChunkData'."
    assert "ChunkData" in content, "main_test.go does not call 'ChunkData'."
    assert "A" in content and "B" in content and "C" in content and "D" in content, "main_test.go does not seem to test the required input data."

def test_main_go_fixes():
    main_file = "/home/user/logchunker/main.go"
    assert os.path.isfile(main_file), f"{main_file} is missing."

    with open(main_file, 'r') as f:
        content = f.read()

    assert "end = len(data) + 1" not in content, "The algorithmic bug 'end = len(data) + 1' is still present in main.go."
    assert "var count string = len(chunks)" not in content, "The compiler error 'var count string = len(chunks)' is still present in main.go."