# test_final_state.py

import os
import pytest

def test_processor_rs_exists():
    path = "/home/user/processor.rs"
    assert os.path.isfile(path), f"Rust source file is missing at {path}"

def test_summary_txt_exists():
    path = "/home/user/summary.txt"
    assert os.path.isfile(path), f"Output file is missing at {path}"

def test_summary_txt_content():
    path = "/home/user/summary.txt"
    if not os.path.isfile(path):
        pytest.fail(f"Cannot check content, {path} does not exist.")

    with open(path, "r") as f:
        content = f.read().strip()

    lines = content.splitlines()
    assert len(lines) >= 2, f"Expected at least 2 lines in {path}, found {len(lines)}"

    mean_line = lines[0].strip()
    top3_line = lines[1].strip()

    assert mean_line == "Mean Similarity: 0.3705", f"Incorrect Mean Similarity line. Got: {mean_line}"
    assert top3_line == "Top 3: [1, 4, 2]", f"Incorrect Top 3 line. Got: {top3_line}"