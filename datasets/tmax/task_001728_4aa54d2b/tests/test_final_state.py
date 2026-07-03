# test_final_state.py

import os
import pytest

def test_terminated_containers_file():
    txt_path = "/home/user/terminated_containers.txt"
    assert os.path.isfile(txt_path), f"Output file {txt_path} is missing."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_containers = ["C-102", "C-104"]

    # Check that exactly the expected containers are present, order does not matter
    assert sorted(lines) == sorted(expected_containers), (
        f"Expected {txt_path} to contain exactly {expected_containers}, "
        f"but found {lines}."
    )

def test_cloud_db_state():
    db_path = "/home/user/.cloud_db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    with open(db_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    terminated_in_db = []
    for line in lines:
        parts = line.split(',')
        if len(parts) == 5 and parts[4] == "terminated":
            terminated_in_db.append(parts[0])

    expected_terminated = ["C-102", "C-104"]

    assert sorted(terminated_in_db) == sorted(expected_terminated), (
        f"Expected exactly {expected_terminated} to be marked as terminated in {db_path}, "
        f"but found {terminated_in_db}."
    )

def test_cost_pipeline_script_exists_and_executable():
    script_path = "/home/user/cost_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Pipeline script {script_path} is not executable."

def test_cloud_session_exists():
    session_path = "/home/user/.cloud_session"
    assert os.path.isfile(session_path), (
        f"Session file {session_path} is missing. "
        "The script must successfully log in using the cloud-manager tool."
    )