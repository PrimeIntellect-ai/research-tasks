# test_final_state.py

import os
import json
import pytest

def test_recover_script_exists():
    script_path = "/home/user/app/recover.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_recovered_csv_content():
    csv_path = "/home/user/app/recovered.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "100,ADD,50,150",
        "101,SUB,10,111",
        "102,ADD,20,122",
        "104,ADD,15,119",
        "107,ADD,10,117"
    ]

    assert lines == expected_lines, f"The content of {csv_path} does not match the expected valid lines."

def test_current_state_json():
    json_path = "/home/user/app/current_state.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    assert data.get("total") == 85, f"Expected total in {json_path} to be 85, but got {data.get('total')}."

def test_state_diff_exists_and_valid():
    diff_path = "/home/user/app/state.diff"
    assert os.path.isfile(diff_path), f"The file {diff_path} does not exist."

    with open(diff_path, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, f"{diff_path} does not appear to be a unified diff."
    assert "-{\"total\": 60}" in content or "-{\"total\":60}" in content.replace(" ", ""), f"{diff_path} does not show the removal of the old state."
    assert "+{\"total\": 85}" in content or "+{\"total\":85}" in content.replace(" ", ""), f"{diff_path} does not show the addition of the new state."