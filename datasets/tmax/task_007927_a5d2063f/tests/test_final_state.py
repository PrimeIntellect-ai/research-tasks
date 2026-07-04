# test_final_state.py

import os
import pytest

APP_DIR = "/home/user/monitor_app"

def test_secrets_recovered():
    secrets_path = os.path.join(APP_DIR, "secrets.env")
    assert os.path.isfile(secrets_path), f"Secrets file not found at {secrets_path}"

    with open(secrets_path, "r") as f:
        content = f.read()

    assert "super_secret_uptime_key_992" in content, (
        f"The recovered API key was not found in {secrets_path}. "
        "Expected to find 'super_secret_uptime_key_992' in the file."
    )

def test_build_success():
    log_path = os.path.join(APP_DIR, "build_success.log")
    assert os.path.isfile(log_path), (
        f"Build success log not found at {log_path}. "
        "The build script may not have executed successfully or was not fixed."
    )

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "Build complete" in content, (
        f"The build success log {log_path} does not contain the expected text 'Build complete.'."
    )

def test_query_result():
    query_result_path = os.path.join(APP_DIR, "query_result.txt")
    assert os.path.isfile(query_result_path), (
        f"Query result file not found at {query_result_path}. "
        "Did you run the fixed ingest.sh script and redirect its output?"
    )

    with open(query_result_path, "r") as f:
        content = f.read().strip()

    assert content == "3", (
        f"Expected the query result to be exactly '3', but found '{content}'. "
        "The ingest script's SQLite query or filtering logic may still be incorrect."
    )

def test_alert_race_condition_fixed():
    alert_state_path = os.path.join(APP_DIR, "alert_state.txt")
    assert os.path.isfile(alert_state_path), f"Alert state file not found at {alert_state_path}"

    with open(alert_state_path, "r") as f:
        content = f.read().strip()

    assert content == "50", (
        f"Expected the alert state counter to be exactly '50', but found '{content}'. "
        "The race condition in alert.sh was not properly fixed using a file lock."
    )