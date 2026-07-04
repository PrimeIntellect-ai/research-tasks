# test_final_state.py

import os
import pytest

def test_executable_compiled():
    path = "/home/user/incident/telemetry_parser"
    assert os.path.isfile(path), f"The executable '{path}' was not found. Did you fix build.sh and run it?"
    assert os.access(path, os.X_OK), f"The file '{path}' is not executable."

def test_postmortem_file_exists():
    path = "/home/user/postmortem.txt"
    assert os.path.isfile(path), f"The post-mortem report '{path}' was not created."

def test_postmortem_contents():
    path = "/home/user/postmortem.txt"
    assert os.path.isfile(path), f"The post-mortem report '{path}' was not created."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = "DeviceID: SENSOR-X99\nLength: 9999999"

    # Normalize line endings and strip trailing whitespaces
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines()]

    assert content_lines == expected_lines, (
        f"The contents of '{path}' do not match the expected format or values.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{content}"
    )