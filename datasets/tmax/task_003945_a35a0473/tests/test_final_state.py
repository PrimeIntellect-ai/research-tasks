# test_final_state.py

import os
import stat
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/find_path.sh"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_output_A_E():
    try:
        result = subprocess.run(
            [SCRIPT_PATH, "A", "E"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed with error: {e.stderr}")

    try:
        output_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON. Output was:\n{result.stdout}")

    expected_json = [
        {"step": 1, "id": "A", "title": "Paper A", "year": 2000},
        {"step": 2, "id": "B", "title": "Paper B", "year": 2001},
        {"step": 3, "id": "D", "title": "Paper D", "year": 2003},
        {"step": 4, "id": "E", "title": "Paper E", "year": 2004}
    ]

    assert output_json == expected_json, f"Output JSON for A -> E did not match expected.\nExpected: {expected_json}\nGot: {output_json}"

def test_script_output_A_F():
    try:
        result = subprocess.run(
            [SCRIPT_PATH, "A", "F"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed with error: {e.stderr}")

    try:
        output_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON. Output was:\n{result.stdout}")

    expected_json = [
        {"step": 1, "id": "A", "title": "Paper A", "year": 2000},
        {"step": 2, "id": "C", "title": "Paper C", "year": 2002},
        {"step": 3, "id": "F", "title": "Paper F", "year": 2005}
    ]

    assert output_json == expected_json, f"Output JSON for A -> F did not match expected.\nExpected: {expected_json}\nGot: {output_json}"