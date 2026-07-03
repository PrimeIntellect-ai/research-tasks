# test_final_state.py

import os
import re
import pytest

def test_processor_go_fixed():
    path = "/home/user/processor.go"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "float32" not in content, "The source code in processor.go still contains 'float32'. It should be completely replaced with 64-bit precision types."
    assert "float64" in content or "strconv.ParseFloat(scanner.Text(), 64)" in content, "The source code does not appear to use 64-bit precision (float64) as requested."

def test_processor_binary_exists():
    path = "/home/user/processor"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist. Did you run 'go build'?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_results_file_content():
    path = "/home/user/results.txt"
    assert os.path.isfile(path), f"Results file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "Processing query 4" in content, "results.txt is missing output for query 4."
    assert "Processing query 5" in content, "results.txt is missing output for query 5."

    # Check that the livelock was resolved and it successfully reached 120
    assert re.search(r"Success:\s*120\.000", content), "results.txt does not show successful completion for target 120.0 (query 4). Livelock might still be present."

    # Check that it successfully processed the final query
    assert re.search(r"Success:\s*0\.001000", content), "results.txt does not show successful completion for target 0.001 (query 5)."