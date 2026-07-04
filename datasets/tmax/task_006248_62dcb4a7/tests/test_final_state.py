# test_final_state.py

import os
import pytest

def test_parsed_services_csv():
    csv_path = "/home/user/parsed_services.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "cont-db,DB_USER=root,/home/user/mocks/run_db.sh",
        "cont-api,API_ENV=prod,/home/user/mocks/run_api.sh",
        "cont-cache,CACHE_SIZE=10,/home/user/mocks/run_cache.sh"
    ]

    assert lines == expected_lines, f"The contents of {csv_path} do not match the expected output."

def test_supervisor_script_exists():
    script_path = "/home/user/container_supervisor.py"
    assert os.path.isfile(script_path), f"The Python script {script_path} does not exist."

def test_supervisor_log():
    log_path = "/home/user/supervisor.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[cont-db] SUCCESS",
        "[cont-api] SUCCESS",
        "[cont-cache] FAILED"
    ]

    assert lines == expected_lines, f"The contents of {log_path} do not match the expected output."