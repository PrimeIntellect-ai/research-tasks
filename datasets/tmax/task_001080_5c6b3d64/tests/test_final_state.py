# test_final_state.py

import os
import json
import pytest

def test_server_conf_exists_and_correct():
    conf_path = "/home/user/server_conf.json"
    assert os.path.exists(conf_path), f"Configuration file {conf_path} does not exist."

    with open(conf_path, 'r') as f:
        try:
            conf_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{conf_path} is not valid JSON.")

    assert "port" in conf_data, f"'port' key missing in {conf_path}."
    assert conf_data["port"] == 9042, f"Expected port 9042 in {conf_path}, but got {conf_data['port']}."

def test_server_py_fixed():
    server_path = "/home/user/server.py"
    assert os.path.exists(server_path), f"{server_path} does not exist."

    with open(server_path, 'r') as f:
        content = f.read()

    # Check for some form of locking (Lock, RLock, Semaphore)
    assert "Lock" in content or "Semaphore" in content, (
        f"{server_path} does not appear to use threading locks to fix the race condition."
    )

def test_metrics_out_exists_and_correct():
    out_path = "/home/user/metrics_out.json"
    assert os.path.exists(out_path), (
        f"Output file {out_path} does not exist. The server may not have processed the SHUTDOWN packet."
    )

    with open(out_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{out_path} is not valid JSON.")

    expected = {
        "metric_1": 200,
        "metric_2": 200,
        "metric_3": 200,
        "metric_4": 200,
        "metric_5": 200
    }

    assert data == expected, (
        f"Contents of {out_path} do not match the expected aggregated metrics. "
        f"Expected {expected}, but got {data}. "
        "The race condition may not be fully fixed."
    )