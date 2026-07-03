# test_final_state.py

import os
import pytest

def test_clean_logs_created_and_sorted():
    clean_logs_path = "/home/user/clean_logs.txt"
    assert os.path.isfile(clean_logs_path), f"File {clean_logs_path} is missing."

    with open(clean_logs_path, "rb") as f:
        content = f.read()

    # Check for non-ASCII characters
    try:
        text_content = content.decode('ascii')
    except UnicodeDecodeError:
        pytest.fail(f"File {clean_logs_path} contains non-ASCII characters.")

    lines = text_content.strip().split('\n')

    # Check if lines are sorted by timestamp
    timestamps = []
    for line in lines:
        if line.strip():
            parts = line.split()
            assert len(parts) >= 1, f"Line format incorrect: {line}"
            timestamps.append(parts[0])

    assert timestamps == sorted(timestamps), f"File {clean_logs_path} is not sorted chronologically."

    # Check if correct number of lines exist (5 valid lines from original)
    assert len(timestamps) == 5, f"Expected 5 clean log lines, found {len(timestamps)}."

def test_config_file_created_and_correct():
    config_path = "/home/user/.config/metrics.ini"
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    # Remove whitespace/newlines to check assignment
    clean_content = content.replace(" ", "").replace("\"", "").replace("'", "").strip()
    assert "FACTOR=3" in clean_content.split('\n'), f"Configuration file {config_path} does not contain FACTOR=3."

def test_answer_file_correct():
    answer_path = "/home/user/answer.txt"
    assert os.path.isfile(answer_path), f"File {answer_path} is missing. Did you run process.sh?"

    with open(answer_path, "r") as f:
        content = f.read().strip()

    assert content == "2700", f"Expected answer 2700 in {answer_path}, but got {content}."