# test_final_state.py

import os

def test_server_built():
    """Test that the server binary has been successfully built."""
    server_path = "/home/user/server_src/server"
    assert os.path.isfile(server_path), f"The server binary was not found at {server_path}. Did you run make?"
    assert os.access(server_path, os.X_OK), f"The file at {server_path} is not executable."

def test_report_exists():
    """Test that the report.txt file has been created."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

def test_report_content():
    """Test that the report.txt file contains the correct answers."""
    report_path = "/home/user/report.txt"

    with open(report_path, "r") as f:
        content = f.read().strip()

    lines = content.split("\n")
    assert len(lines) == 3, f"Expected exactly 3 lines in report.txt, but found {len(lines)}."

    # Line 1: The exact flag added to the Makefile to fix the linker error
    assert lines[0].strip() == "-lm", f"Line 1 is incorrect. Expected '-lm', got '{lines[0].strip()}'."

    # Line 2: The exact string payload extracted from the PCAP file
    expected_payload = "OVERFLOW_PAYLOAD_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    assert lines[1].strip() == expected_payload, f"Line 2 is incorrect. Expected '{expected_payload}', got '{lines[1].strip()}'."

    # Line 3: The exact name of the C function where the segmentation fault occurs
    assert lines[2].strip() == "log_message", f"Line 3 is incorrect. Expected 'log_message', got '{lines[2].strip()}'."