# test_final_state.py

import os
import pytest

def test_parsed_payloads_exists():
    path = "/home/user/parsed_payloads.txt"
    assert os.path.isfile(path), f"The output file {path} was not created."

def test_parsed_payloads_content():
    path = "/home/user/parsed_payloads.txt"
    assert os.path.isfile(path), f"The output file {path} was not created."

    expected_lines = [
        "Service started cleanly",
        "Missing fallback configuration",
        "Failed to parse payload: <xml><error>Unclosed tag</error></xml>",
        "Request complete: status -> success",
        "Shutdown sequence initiated"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        "The contents of parsed_payloads.txt do not match the expected payloads. "
        f"Expected {len(expected_lines)} lines, got {len(actual_lines)}. "
        "Check your parsing logic for off-by-one errors and edge cases."
    )

def test_server_log_unmodified():
    path = "/home/user/server.log"
    assert os.path.isfile(path), f"Server log file is missing: {path}"

    expected_content = (
        "[08:00:01] (INFO) - Message: <Service started cleanly>\n"
        "[08:00:05] (WARN) - Message: <Missing fallback configuration>\n"
        "[08:00:10] (ERROR) - Message: <Failed to parse payload: <xml><error>Unclosed tag</error></xml>>\n"
        "[08:00:15] (INFO) - Message: <Request complete: status -> success>\n"
        "[08:00:20] (INFO) - Message: <Shutdown sequence initiated>\n"
    )

    with open(path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), "The original server.log file was modified. It should remain unchanged."