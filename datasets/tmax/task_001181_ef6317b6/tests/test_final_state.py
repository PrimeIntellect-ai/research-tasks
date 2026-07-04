# test_final_state.py

import os
import json
import pytest

def test_deploy_script_exists():
    assert os.path.isfile('/home/user/deploy.py'), "The deployment script /home/user/deploy.py does not exist."

def test_deploy_log_content():
    log_path = '/home/user/deploy.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Check overall structure and key events
    assert "INFO: Backup inst1" in lines, "Missing backup log for inst1."
    assert "INFO: Update inst1" in lines, "Missing update log for inst1."
    assert "INFO: Backup inst2" in lines, "Missing backup log for inst2."
    assert "INFO: Update inst2" in lines, "Missing update log for inst2."

    assert "INFO: Validate inst1 - SUCCESS" in lines, "Missing successful validation log for inst1."
    assert "INFO: Validate inst2 - SUCCESS" in lines, "Missing successful validation log for inst2."

    assert "INFO: Backup inst3" in lines, "Missing backup log for inst3."
    assert "INFO: Update inst3" in lines, "Missing update log for inst3."
    assert "INFO: Backup inst4" in lines, "Missing backup log for inst4."
    assert "INFO: Update inst4" in lines, "Missing update log for inst4."

    assert "ERROR: Validate inst4 - FAILED" in lines, "Missing failed validation log for inst4."

    # Check rollback order
    try:
        idx_rb4 = lines.index("INFO: Rollback inst4")
        idx_rb3 = lines.index("INFO: Rollback inst3")
        idx_rb2 = lines.index("INFO: Rollback inst2")
        idx_rb1 = lines.index("INFO: Rollback inst1")
        idx_complete = lines.index("CRITICAL: Rollback complete")

        assert idx_rb4 < idx_rb3 < idx_rb2 < idx_rb1 < idx_complete, "Rollback logs are not in the exact reverse order of updates."
    except ValueError as e:
        pytest.fail(f"Missing rollback log entries or not in expected format: {e}")

def test_configs_restored():
    expected_config = {"version": "1.0", "theme": "blue"}
    for i in range(1, 6):
        config_path = f"/home/user/instances/inst{i}/config.json"
        assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

        with open(config_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"Config file {config_path} is not valid JSON.")

        assert data == expected_config, f"Config file {config_path} was not restored to the initial state."

def test_backups_created():
    for i in range(1, 5):
        backup_path = f"/home/user/backups/inst{i}_config.json.bak"
        assert os.path.isfile(backup_path), f"Backup file {backup_path} should exist."

    backup_path_5 = "/home/user/backups/inst5_config.json.bak"
    assert not os.path.exists(backup_path_5), f"Backup file {backup_path_5} should not exist since inst5 was never reached."