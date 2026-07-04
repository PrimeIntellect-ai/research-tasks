# test_final_state.py

import os
import pytest

def test_env_txt_content():
    env_path = "/home/user/pipeline/env.txt"
    assert os.path.isfile(env_path), f"File {env_path} is missing."

    with open(env_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {env_path}, but found {len(lines)}."
    assert lines[0] == "X_PIPELINE_AUTH_KEY_V2", f"Expected first line to be 'X_PIPELINE_AUTH_KEY_V2', got '{lines[0]}'."
    assert lines[1] == "CS_8x99y2z1a4", f"Expected second line to be 'CS_8x99y2z1a4', got '{lines[1]}'."

def test_recover_go_exists():
    go_path = "/home/user/pipeline/recover.go"
    assert os.path.isfile(go_path), f"Go source file {go_path} is missing."

def test_output_log_content():
    output_path = "/home/user/pipeline/data/output.log"
    assert os.path.isfile(output_path), f"Output log {output_path} is missing."

    expected_lines = [
        "[AUTH] User login successful CS_8x99y2z1a4",
        "[AUTH] Token refreshed CS_8x99y2z1a4"
    ]

    with open(output_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert actual_lines == expected_lines, f"Expected output log lines {expected_lines}, but got {actual_lines}."