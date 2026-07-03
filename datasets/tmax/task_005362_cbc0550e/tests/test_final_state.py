# test_final_state.py

import os
import json
import sqlite3
import requests
import pytest
import math

def test_config_json_secret_recovered():
    config_path = "/app/video_service/config.json"
    assert os.path.isfile(config_path), f"File {config_path} does not exist."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} is not valid JSON.")

    assert "api_secret" in config, "Key 'api_secret' not found in config.json."
    assert config["api_secret"] == "sec_99abf210d", "The recovered API secret is incorrect."

def test_database_recovered():
    db_path = "/app/video_service/db/settings.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM thresholds")
        rows = cursor.fetchall()
        assert len(rows) > 0, "The 'thresholds' table is empty. Database recovery might have failed."
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Failed to read 'thresholds' table from database: {e}")
    finally:
        conn.close()

def test_log_file_contents():
    log_path = "/app/video_service/found_timestamps.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    floats = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                floats.append(float(line))
            except ValueError:
                pytest.fail(f"Log file contains non-float value: {line}")

    expected = [1.5, 3.0, 4.5]
    assert len(floats) == len(expected), f"Expected {len(expected)} timestamps, found {len(floats)}."

    for f_val, e_val in zip(floats, expected):
        assert math.isclose(f_val, e_val, abs_tol=0.01), f"Expected timestamp ~{e_val}, found {f_val}."

def test_service_running_and_responds():
    url = "http://127.0.0.1:8080/api/events"
    headers = {"Authorization": "Bearer sec_99abf210d"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "events" in data, "Response JSON does not contain 'events' key."
    events = data["events"]
    assert isinstance(events, list), "'events' should be a list."

    expected = [1.5, 3.0, 4.5]
    assert len(events) == len(expected), f"Expected {len(expected)} events, got {len(events)}."

    for f_val, e_val in zip(events, expected):
        assert isinstance(f_val, (int, float)), f"Event value {f_val} is not a number."
        assert math.isclose(f_val, e_val, abs_tol=0.01), f"Expected event ~{e_val}, found {f_val}."