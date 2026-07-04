# test_final_state.py

import os
import json
import sqlite3
import re
import pytest

def test_optimize_sql_exists_and_valid():
    """Verify that optimize.sql exists and contains a valid CREATE INDEX statement."""
    sql_path = "/home/user/optimize.sql"
    assert os.path.isfile(sql_path), f"Optimization script not found at {sql_path}."

    with open(sql_path, "r") as f:
        content = f.read().lower()

    assert "create index" in content, "optimize.sql must contain a CREATE INDEX statement."
    assert "on logs" in content or "on \"logs\"" in content or "on `logs`" in content, "The index must be created on the 'logs' table."
    assert "uid" in content, "The index must include the 'uid' column."
    assert "success" in content, "The index must include the 'success' column."

def test_rust_project_exists():
    """Verify that the Rust project was initialized."""
    cargo_toml = "/home/user/auditor/Cargo.toml"
    main_rs = "/home/user/auditor/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project not found: {cargo_toml} is missing."
    assert os.path.isfile(main_rs), f"Rust source not found: {main_rs} is missing."

def test_report_json_exists_and_valid():
    """Verify that the report JSON file is generated correctly for uid 42."""
    report_path = "/home/user/report_42.json"
    assert os.path.isfile(report_path), f"Report file not found at {report_path}."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be an array of objects."

    expected = [
        {"target_system": "Vault A", "unauthorized_attempts": 2},
        {"target_system": "Vault B", "unauthorized_attempts": 1},
        {"target_system": "Vault C", "unauthorized_attempts": 3}
    ]

    # Sort both just in case, though the prompt required sorting by target_system
    data_sorted = sorted(data, key=lambda x: x.get("target_system", ""))
    expected_sorted = sorted(expected, key=lambda x: x["target_system"])

    assert data_sorted == expected_sorted, f"Report data mismatch. Expected {expected_sorted}, got {data_sorted}."

def test_db_index_created():
    """Verify that the index was actually applied to the database."""
    db_path = "/home/user/compliance.db"
    assert os.path.isfile(db_path), f"Database file missing at {db_path}."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='logs'")
    indexes = cur.fetchall()
    conn.close()

    # Filter out auto-indexes (like sqlite_autoindex)
    user_indexes = [idx for idx in indexes if idx[1] is not None]

    assert len(user_indexes) > 0, "No custom index was found on the 'logs' table in the database."

    # Check if the applied index matches the requirements
    valid_index_found = False
    for name, sql in user_indexes:
        sql_lower = sql.lower()
        if "uid" in sql_lower and "success" in sql_lower:
            valid_index_found = True
            break

    assert valid_index_found, "The index applied to the database does not include both 'uid' and 'success' columns."