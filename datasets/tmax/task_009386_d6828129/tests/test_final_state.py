# test_final_state.py

import os
import pytest

def test_script_exists():
    script_path = "/home/user/get_latest_prod.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_output_file_exists():
    output_path = "/home/user/latest_versions.log"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_output_file_contents():
    output_path = "/home/user/latest_versions.log"
    expected_lines = [
        "AnalyticsModule:2.0.0-beta",
        "ChatApp:1.0.0",
        "PaymentApp:1.3.2"
    ]

    with open(output_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {output_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )