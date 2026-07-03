# test_final_state.py
import os
import pytest

def count_codepoints(s):
    # In Python 3, len() on a string counts Unicode codepoints
    return len(s)

def compute_expected_anomalies(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    history = []
    last_accepted = None
    out = []

    for i, line in enumerate(lines):
        N = i + 1
        stripped = line.strip(" \t\r\n")
        if not stripped:
            continue
        if stripped == last_accepted:
            continue

        L = count_codepoints(stripped)

        if len(history) >= 3:
            avg = sum(history[-3:]) // 3
            if L > 2 * avg:
                out.append(f"Line {N}: {L} codepoints\n")

        history.append(L)
        last_accepted = stripped

    return out

def test_c_program_exists():
    src_path = "/home/user/detector.c"
    exe_path = "/home/user/detector"
    assert os.path.exists(src_path), f"The source file {src_path} is missing."
    assert os.path.exists(exe_path), f"The compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_anomalies_file_exists():
    anomalies_path = "/home/user/anomalies.txt"
    assert os.path.exists(anomalies_path), f"The file {anomalies_path} was not created."
    assert os.path.isfile(anomalies_path), f"{anomalies_path} is not a regular file."

def test_anomalies_content():
    input_path = "/home/user/input.txt"
    anomalies_path = "/home/user/anomalies.txt"

    assert os.path.exists(input_path), f"Input file {input_path} is missing, cannot compute expected anomalies."
    assert os.path.exists(anomalies_path), f"Anomalies file {anomalies_path} is missing."

    expected_lines = compute_expected_anomalies(input_path)

    with open(anomalies_path, "r", encoding="utf-8") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"The contents of {anomalies_path} do not match the expected output.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Actual:\n{''.join(actual_lines)}"
    )