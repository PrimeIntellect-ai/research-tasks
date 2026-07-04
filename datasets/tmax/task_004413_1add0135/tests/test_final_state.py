# test_final_state.py

import os
import json
import sqlite3
import re
import pytest

WORKSPACE = "/home/user/legacy_aggregator"
REPORT_PATH = "/home/user/debug_report.json"
INPUT_CSV = os.path.join(WORKSPACE, "input_data.csv")
CRASH_DMP = os.path.join(WORKSPACE, "crash.dmp")
DB_PATH = os.path.join(WORKSPACE, "results.db")
REQ_PATH = os.path.join(WORKSPACE, "requirements.txt")
VENV_PATH = os.path.join(WORKSPACE, "venv")

def get_expected_score():
    if not os.path.exists(INPUT_CSV):
        return 0
    total = 0
    with open(INPUT_CSV, 'r') as f:
        header = f.readline()
        for line in f:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    total += int(parts[1])
    return total

def get_expected_token():
    if not os.path.exists(CRASH_DMP):
        return ""
    with open(CRASH_DMP, 'rb') as f:
        content = f.read()
        match = re.search(b'AUTH_TOKEN=([a-zA-Z0-9]{16})', content)
        if match:
            return match.group(1).decode('utf-8')
    return ""

def test_report_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_PATH} is not valid JSON.")

    expected_token = get_expected_token()
    expected_score = get_expected_score()

    assert "extracted_token" in report, "Missing 'extracted_token' in report."
    assert report["extracted_token"] == expected_token, f"Incorrect extracted_token. Expected {expected_token}."

    assert "correct_total_score" in report, "Missing 'correct_total_score' in report."
    assert report["correct_total_score"] == expected_score, f"Incorrect correct_total_score. Expected {expected_score}."

    assert "fixed_urllib3_version" in report, "Missing 'fixed_urllib3_version' in report."
    assert isinstance(report["fixed_urllib3_version"], str), "fixed_urllib3_version must be a string."

def test_database_results():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."
    expected_score = get_expected_score()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT total_score FROM aggregate")
        row = c.fetchone()
        assert row is not None, "No data found in aggregate table."
        db_score = row[0]
        assert db_score == expected_score, f"Database total_score {db_score} does not match expected {expected_score}. Race condition may not be fixed."
    except sqlite3.OperationalError as e:
        pytest.fail(f"Database query failed: {e}")
    finally:
        conn.close()

def test_venv_exists():
    assert os.path.isdir(VENV_PATH), f"Virtual environment directory {VENV_PATH} does not exist."
    bin_dir = os.path.join(VENV_PATH, "bin")
    assert os.path.isdir(bin_dir), f"Virtual environment bin directory {bin_dir} does not exist."