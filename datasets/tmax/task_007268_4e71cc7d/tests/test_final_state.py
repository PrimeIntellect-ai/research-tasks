# test_final_state.py

import os
import pytest

def test_bad_metric_txt():
    path = "/home/user/bad_metric.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "SRE_CORRUPT_0x8F9A", f"Incorrect content in {path}: {content}"

def test_cleaned_metrics_log():
    path = "/home/user/cleaned_metrics.log"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "2023-10-12T10:00:00Z,OK,METRIC_NODE_A_001\n"
        "2023-10-12T10:00:05Z,OK,METRIC_NODE_B_002\n"
        "2023-10-12T10:00:10Z,WARN,METRIC_NODE_C_003\n"
        "2023-10-12T10:00:20Z,OK,METRIC_NODE_A_004"
    )
    assert content == expected_content, f"Content of {path} is incorrect. Expected lines without the corrupt metric."

def test_metrics_diff():
    path = "/home/user/metrics.diff"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "--- /home/user/raw_metrics.log" in content or "--- " in content, f"{path} does not look like a unified diff."
    assert "+++ /home/user/cleaned_metrics.log" in content or "+++ " in content, f"{path} does not look like a unified diff."
    assert "-2023-10-12T10:00:15Z,ERR,SRE_CORRUPT_0x8F9A" in content, f"{path} does not show the removal of the corrupt metric line."

def test_cleaner_rs_exists():
    path = "/home/user/cleaner.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "fn main" in content, f"{path} does not appear to be a valid Rust script (missing fn main)."