# test_final_state.py

import os
import json
import sqlite3
import pytest

OPTIMIZE_SQL_PATH = '/home/user/optimize.sql'
ANALYZE_PY_PATH = '/home/user/analyze.py'
SUSPECT_JSON_PATH = '/home/user/suspect.json'
DB_PATH = '/home/user/audit.db'

def test_optimize_sql_exists_and_valid():
    """Test that optimize.sql is created and contains CREATE INDEX statements."""
    assert os.path.exists(OPTIMIZE_SQL_PATH), f"{OPTIMIZE_SQL_PATH} does not exist."
    with open(OPTIMIZE_SQL_PATH, 'r') as f:
        content = f.read().lower()

    assert "create index" in content, "optimize.sql does not contain CREATE INDEX statements."

    # Check if the indexes were actually created in the DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='raw_events'")
    indexes = c.fetchall()
    conn.close()

    # The user might not have executed optimize.sql, but the task says "Create a SQL script... that creates an index".
    # We will just verify the SQL script contents as requested by the prompt.
    assert "payload" in content or "routing" in content, "optimize.sql does not seem to reference the correct JSON paths."

def test_analyze_py_exists():
    """Test that analyze.py was created."""
    assert os.path.exists(ANALYZE_PY_PATH), f"{ANALYZE_PY_PATH} does not exist."
    assert os.path.isfile(ANALYZE_PY_PATH), f"{ANALYZE_PY_PATH} is not a file."

def test_suspect_json_correct():
    """Test that suspect.json exists and contains the correct suspect and score."""
    assert os.path.exists(SUSPECT_JSON_PATH), f"{SUSPECT_JSON_PATH} does not exist."

    with open(SUSPECT_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUSPECT_JSON_PATH} does not contain valid JSON.")

    assert "suspect_account" in data, "suspect.json missing 'suspect_account' key."
    assert "pagerank_score" in data, "suspect.json missing 'pagerank_score' key."

    assert data["suspect_account"] == "ACT_C", f"Expected suspect_account to be 'ACT_C', but got '{data['suspect_account']}'."

    score = data["pagerank_score"]
    assert isinstance(score, (int, float)), "pagerank_score must be a number."

    # Check if score is approximately correct (around 0.2312)
    assert abs(score - 0.2312) < 0.05, f"Expected pagerank_score to be around 0.2312, but got {score}."