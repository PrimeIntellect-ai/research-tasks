# test_final_state.py

import os
import json
import sqlite3
import pytest
import re

MATH_APP_DIR = "/home/user/math_app"
SETUP_PY = os.path.join(MATH_APP_DIR, "setup.py")
DATA_DB = os.path.join(MATH_APP_DIR, "data.db")
FINAL_JSON = "/home/user/final_data.json"

def test_setup_py_fixed():
    """Verify that setup.py was modified to include the math library."""
    assert os.path.isfile(SETUP_PY), f"{SETUP_PY} is missing."
    with open(SETUP_PY, 'r') as f:
        content = f.read()

    # Check if libraries=['m'] or similar is present
    assert re.search(r"libraries\s*=\s*\[\s*['\"]m['\"]\s*\]", content), \
        "setup.py does not appear to link against the math library (missing libraries=['m'])."

def test_database_schema_migrated():
    """Verify the database schema is updated correctly."""
    assert os.path.isfile(DATA_DB), f"{DATA_DB} is missing."
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()

    c.execute("PRAGMA table_info(calculations)")
    columns = {row[1]: row[2].upper() for row in c.fetchall()}
    conn.close()

    assert "id" in columns, "Column 'id' missing in calculations table."
    assert "input_val" in columns, "Column 'input_val' missing in calculations table."
    assert "result" in columns, "Column 'result' missing in calculations table."
    assert "algo_version" in columns, "Column 'algo_version' missing in calculations table."

def test_final_json_output():
    """Verify the final output JSON file contains the correct data."""
    assert os.path.isfile(FINAL_JSON), f"{FINAL_JSON} is missing."

    with open(FINAL_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{FINAL_JSON} is not valid JSON.")

    assert isinstance(data, list), "JSON root must be a list."
    assert len(data) == 5, f"Expected 5 rows in JSON, got {len(data)}."

    # Check legacy data
    legacy_results = [3.14, 2.71]
    for i in range(2):
        row = data[i]
        assert row.get("input_val") == 0.0, f"Row {i+1} input_val should be 0.0"
        assert row.get("result") == legacy_results[i], f"Row {i+1} result should be {legacy_results[i]}"
        assert row.get("algo_version") == "1.0", f"Row {i+1} algo_version should be '1.0'"

    # Check new calculations
    new_inputs = [16.0, 64.0, 144.0]
    new_results = [4.0, 8.0, 12.0]
    for i in range(3):
        row = data[i+2]
        assert row.get("input_val") == new_inputs[i], f"Row {i+3} input_val should be {new_inputs[i]}"
        assert row.get("result") == new_results[i], f"Row {i+3} result should be {new_results[i]}"
        assert row.get("algo_version") == "2.0", f"Row {i+3} algo_version should be '2.0'"