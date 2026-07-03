# test_final_state.py
import os

def test_final_output_exists():
    assert os.path.isfile("/home/user/data/final_output.csv"), "The file /home/user/data/final_output.csv does not exist."

def test_final_output_correct():
    final_output_path = "/home/user/data/final_output.csv"
    expected_output_path = "/home/user/data/expected_output.csv"

    assert os.path.isfile(expected_output_path), f"Expected output file {expected_output_path} is missing."

    with open(final_output_path, "r") as f:
        final_content = f.read()
    with open(expected_output_path, "r") as f:
        expected_content = f.read()

    assert final_content == expected_content, "The contents of final_output.csv do not match expected_output.csv."

def test_debug_report_exists():
    assert os.path.isfile("/home/user/debug_report.txt"), "The file /home/user/debug_report.txt does not exist."

def test_debug_report_content():
    with open("/home/user/debug_report.txt", "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in debug_report.txt, but found {len(lines)}."
    assert lines[0] == "records", f"Expected the first line to be 'records', but got '{lines[0]}'."
    assert lines[1] == "float", f"Expected the second line to be 'float', but got '{lines[1]}'."