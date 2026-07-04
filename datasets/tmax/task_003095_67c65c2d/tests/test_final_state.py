# test_final_state.py

import os
import json
import pytest

CONFIG_DIR = "/home/user/config_backups"
AUDIT_LOG = "/home/user/redaction_audit.log"
MASTER_JSON = "/home/user/master_config.json"
CONSOLIDATE_SCRIPT = "/home/user/consolidate.py"

def test_phase1_merging():
    merged_file = os.path.join(CONFIG_DIR, "app_server.cfg")
    assert os.path.isfile(merged_file), f"Merged file {merged_file} does not exist."

    for i in range(1, 4):
        part_file = os.path.join(CONFIG_DIR, f"app_server.part{i}.cfg")
        assert not os.path.exists(part_file), f"Part file {part_file} was not deleted."

def test_phase1_renaming():
    db_ini = os.path.join(CONFIG_DIR, "db_config.ini")
    db_txt = os.path.join(CONFIG_DIR, "db_config.txt")
    notes_txt = os.path.join(CONFIG_DIR, "notes.txt")

    assert os.path.isfile(db_ini), f"File {db_ini} does not exist. Renaming failed."
    assert not os.path.exists(db_txt), f"File {db_txt} still exists. It should have been renamed."
    assert os.path.isfile(notes_txt), f"File {notes_txt} should not have been renamed or deleted."

def test_phase2_redaction_audit_log():
    assert os.path.isfile(AUDIT_LOG), f"Audit log {AUDIT_LOG} does not exist."

    with open(AUDIT_LOG, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_entries = [
        "app_server.cfg:5:API_KEY",
        "app_server.cfg:8:password",
        "db_config.ini:7:password",
        "db_config.ini:8:api_key",
        "cache.cfg:4:Password"
    ]

    for entry in expected_entries:
        assert entry in lines, f"Expected entry '{entry}' not found in {AUDIT_LOG}"

    assert len(lines) == len(expected_entries), f"Audit log contains unexpected entries: {lines}"

def test_phase2_file_contents_redacted():
    # Check app_server.cfg
    app_server = os.path.join(CONFIG_DIR, "app_server.cfg")
    with open(app_server, "r") as f:
        content = f.read()
    assert "API_KEY=REDACTED" in content, "app_server.cfg was not properly redacted for API_KEY"
    assert "password=REDACTED" in content, "app_server.cfg was not properly redacted for password"

    # Check db_config.ini
    db_ini = os.path.join(CONFIG_DIR, "db_config.ini")
    with open(db_ini, "r") as f:
        content = f.read()
    assert "password=REDACTED" in content, "db_config.ini was not properly redacted for password"
    assert "api_key=REDACTED" in content, "db_config.ini was not properly redacted for api_key"

    # Check cache.cfg
    cache_cfg = os.path.join(CONFIG_DIR, "cache.cfg")
    with open(cache_cfg, "r") as f:
        content = f.read()
    assert "Password=REDACTED" in content, "cache.cfg was not properly redacted for Password"

def test_phase3_master_json_contents():
    assert os.path.isfile(MASTER_JSON), f"Master JSON file {MASTER_JSON} does not exist."

    with open(MASTER_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {MASTER_JSON} is not valid JSON.")

    expected_data = {
        "app_server.cfg": {
            "host": "127.0.0.1",
            "port": "8080",
            "API_KEY": "REDACTED",
            "max_connections": "500",
            "timeout": "30",
            "password": "REDACTED"
        },
        "cache.cfg": {
            "engine": "redis",
            "memory": "2G",
            "Password": "REDACTED"
        },
        "db_config.ini": {
            "database": {
                "engine": "postgres",
                "host": "10.0.0.5"
            },
            "credentials": {
                "username": "admin",
                "password": "REDACTED",
                "api_key": "REDACTED"
            }
        }
    }

    assert data == expected_data, f"JSON data in {MASTER_JSON} does not match expected output."

def test_phase3_atomic_write_script():
    assert os.path.isfile(CONSOLIDATE_SCRIPT), f"Python script {CONSOLIDATE_SCRIPT} is missing."

    with open(CONSOLIDATE_SCRIPT, "r") as f:
        content = f.read()

    assert "master_config.json.tmp" in content, "Script does not appear to use the required temporary file for atomic writing."
    assert "rename" in content or "replace" in content, "Script does not appear to use an atomic rename operation."