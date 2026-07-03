# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/research_data.db"
JSON_PATH = "/home/user/summary_results.json"

def test_json_file_exists():
    assert os.path.exists(JSON_PATH), f"Output file missing at {JSON_PATH}"
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file"

def test_json_content_and_computation():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    # Compute expected results dynamically from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT t.treatment_arm, AVG(o.recovery_days)
        FROM patient_records p
        JOIN trial_assignments t ON p.p_id = t.fk_patient
        JOIN observation_metrics o ON t.t_id = o.fk_trial
        WHERE p.patient_age >= 30 
          AND p.primary_condition = 'Asthma'
          AND t.treatment_arm IN ('Arm A', 'Arm B', 'Placebo')
        GROUP BY t.treatment_arm
        ORDER BY t.treatment_arm ASC;
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = []
    for arm, avg_days in expected_rows:
        expected_data.append({
            "treatment_arm": arm,
            "avg_recovery_days": round(avg_days, 2)
        })

    # Read the generated JSON
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {JSON_PATH} does not contain valid JSON")

    assert isinstance(data, list), "JSON output must be a list of objects"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}"

    # Check sorting and values
    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert "treatment_arm" in actual, f"Record {i} missing 'treatment_arm' key"
        assert "avg_recovery_days" in actual, f"Record {i} missing 'avg_recovery_days' key"

        assert actual["treatment_arm"] == expected["treatment_arm"], \
            f"Record {i} expected treatment_arm '{expected['treatment_arm']}', got '{actual['treatment_arm']}'"

        # Float comparison
        actual_val = actual["avg_recovery_days"]
        expected_val = expected["avg_recovery_days"]
        assert isinstance(actual_val, (int, float)), f"Record {i} avg_recovery_days must be a number"
        assert abs(actual_val - expected_val) < 0.01, \
            f"Record {i} for {actual['treatment_arm']} expected {expected_val}, got {actual_val}"