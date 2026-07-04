# test_final_state.py

import os
import pytest

def test_fixed_output_exists():
    assert os.path.isfile("/home/user/fixed_output.txt"), "/home/user/fixed_output.txt is missing. Did you save the output?"

def test_fixed_output_content():
    output_path = "/home/user/fixed_output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "File: /home/user/logs/01.log, Type: INFO, Msg: System started successfully",
        "File: /home/user/logs/01.log, Type: WARN, Msg: CPU temperature high",
        "File: /home/user/logs/02.log, Type: ERROR, Msg: Disk full on /dev/sda1",
        "File: /home/user/logs/02.log, Type: INFO, Msg: Recovery initiated",
        "File: /home/user/logs/02.log, Type: REBOOT, Msg: (none)",
        "File: /home/user/logs/03.log, Type: FATAL, Msg: Kernel panic"
    ]

    sorted_actual = sorted(lines)
    sorted_expected = sorted(expected_lines)

    assert sorted_actual == sorted_expected, (
        f"The content of {output_path} does not match the expected output.\n"
        f"Expected (sorted):\n{chr(10).join(sorted_expected)}\n\n"
        f"Got (sorted):\n{chr(10).join(sorted_actual)}"
    )

def test_parser_compiled():
    executable_path = "/home/user/log_tool/parser"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} is missing. Did you run make?"
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."