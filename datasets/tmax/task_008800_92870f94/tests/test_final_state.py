# test_final_state.py

import os
import json
import configparser
import pytest

def test_app_worker_service_dependency_fixed():
    """Verify that app_worker.service has the correct After dependency."""
    service_file = "/home/user/services/app_worker.service"
    assert os.path.exists(service_file), f"Service file {service_file} is missing."

    config = configparser.ConfigParser()
    config.read(service_file)

    assert config.has_section("Unit"), f"Missing [Unit] section in {service_file}."
    assert config.has_option("Unit", "After"), f"Missing 'After' directive in {service_file}."

    after_value = config.get("Unit", "After")
    assert after_value == "auth_server.service", f"Expected After=auth_server.service, got After={after_value}"

def test_startup_success_log():
    """Verify that the startup log exists and indicates success."""
    log_file = "/home/user/startup_success.log"
    assert os.path.exists(log_file), f"Log file {log_file} was not generated."

    with open(log_file, "r") as f:
        content = f.read()

    assert "All services started successfully." in content, "The startup log does not indicate successful startup. Did the services run correctly?"

def test_sync_script_exists():
    """Verify that the sync_auth_users.py script was created."""
    script_file = "/home/user/sync_auth_users.py"
    assert os.path.exists(script_file), f"Script {script_file} was not created."

def test_auth_db_json_content():
    """Verify that auth_db.json is correctly derived from raw_users.txt."""
    raw_file = "/home/user/raw_users.txt"
    db_file = "/home/user/auth_db.json"

    assert os.path.exists(raw_file), f"Raw users file {raw_file} is missing."
    assert os.path.exists(db_file), f"Database file {db_file} was not generated."

    # Derive expected state
    expected_db = {}
    with open(raw_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) == 3:
                username, role, uid_str = parts
                try:
                    uid = int(uid_str)
                    expected_db[username] = {"role": role, "uid": uid}
                except ValueError:
                    pass # Invalid uid

    # Load actual state
    try:
        with open(db_file, "r") as f:
            actual_db = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {db_file} does not contain valid JSON.")

    assert actual_db == expected_db, f"Content of {db_file} does not match the expected derived state from {raw_file}."