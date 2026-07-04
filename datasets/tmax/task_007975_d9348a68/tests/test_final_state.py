# test_final_state.py

import os
import pytest

def test_parse_script_exists():
    script_path = "/home/user/parse.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_bot_changes_output():
    output_path = "/home/user/bot_changes.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    expected_lines = [
        "/etc/cron.d/backup",
        "/etc/nginx/nginx.conf",
        "/etc/redis/redis.conf",
        "/opt/app/config.yaml"
    ]

    with open(output_path, "r") as f:
        content = f.read()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {output_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )