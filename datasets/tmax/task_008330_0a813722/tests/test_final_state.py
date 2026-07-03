# test_final_state.py
import os

def test_alerts_tsv_exists_and_content():
    alerts_path = "/home/user/alerts.tsv"
    assert os.path.exists(alerts_path), f"Output file {alerts_path} does not exist. Did you run your C++ program to generate it?"

    with open(alerts_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Subnet\tHour\tPreviousCount\tCurrentCount",
        "172.16.20\t2023-10-01T15\t60\t10",
        "192.168.1\t2023-10-01T11\t100\t15"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {alerts_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {alerts_path} mismatch.\nExpected: '{expected}'\nGot:      '{actual}'"

def test_cpp_file_exists():
    cpp_path = "/home/user/process_logs.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} does not exist."