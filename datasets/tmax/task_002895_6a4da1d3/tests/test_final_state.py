# test_final_state.py

import os
import sqlite3
import pytest

def test_database_accuracy():
    db_path = '/home/user/cleaned_telemetry.db'
    golden_path = '/tmp/golden_telemetry.csv'

    assert os.path.isfile(db_path), f"Agent's output database not found at {db_path}"
    assert os.path.isfile(golden_path), f"Golden reference file not found at {golden_path}"

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT frame_md5, location_name, vehicle_count FROM telemetry ORDER BY frame_md5")
        agent_rows = c.fetchall()
        conn.close()
    except Exception as e:
        pytest.fail(f"Failed to read agent DB: {e}")

    expected_rows = set()
    with open(golden_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                expected_rows.add((parts[0], parts[1], int(parts[2])))

    assert expected_rows, "Golden reference file is empty or invalid"

    agent_set = set(agent_rows)
    correct_matches = len(expected_rows.intersection(agent_set))
    accuracy = correct_matches / len(expected_rows)

    assert accuracy >= 0.95, f"Accuracy {accuracy:.4f} is below the threshold of 0.95. Expected {len(expected_rows)} rows, got {len(agent_set)} rows with {correct_matches} correct matches."