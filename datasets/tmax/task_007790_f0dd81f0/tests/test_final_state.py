# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_recovered_db_exists_and_valid():
    rec_path = "/home/user/profiler/recovered.db"
    assert os.path.isfile(rec_path), f"The recovered database {rec_path} does not exist."

    try:
        conn = sqlite3.connect(rec_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cpu_usage FROM measurements ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to read from recovered.db. It might still be corrupted or invalid: {e}")

    assert len(rows) == 5, f"Expected 5 measurements in recovered.db, found {len(rows)}."
    expected_cpu_usages = [45.0, 55.0, 65.0, 70.0, 60.0]
    actual_cpu_usages = [r[0] for r in rows]
    assert actual_cpu_usages == expected_cpu_usages, f"Expected CPU usages {expected_cpu_usages}, got {actual_cpu_usages}."

def test_output_json_exists_and_correct():
    out_path = "/home/user/profiler/output.json"
    assert os.path.isfile(out_path), f"The output file {out_path} does not exist. Did you run the script?"

    with open(out_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {out_path} does not contain valid JSON.")

    assert "span" in data, "The output JSON is missing the 'span' key."
    assert "ema" in data, "The output JSON is missing the 'ema' key."

    assert data["span"] == 3, f"Expected span to be 3, got {data['span']}."

    # Compute the expected EMA values
    cpu_usages = [45.0, 55.0, 65.0, 70.0, 60.0]
    span = 3
    alpha = 2.0 / (span + 1)

    expected_ema = []
    for i, val in enumerate(cpu_usages):
        if i == 0:
            expected_ema.append(val)
        else:
            expected_ema.append(alpha * val + (1 - alpha) * expected_ema[-1])

    expected_ema_rounded = [round(x, 2) for x in expected_ema]

    actual_ema = data["ema"]
    assert isinstance(actual_ema, list), "The 'ema' value in output JSON should be a list."
    assert len(actual_ema) == len(expected_ema_rounded), f"Expected {len(expected_ema_rounded)} EMA values, got {len(actual_ema)}."

    for i, (actual, expected) in enumerate(zip(actual_ema, expected_ema_rounded)):
        assert actual == expected, f"EMA value mismatch at index {i}: expected {expected}, got {actual}."

def test_script_is_fixed():
    script_path = "/home/user/profiler/process_metrics.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # The buggy implementation was alpha = (span + 1) / 2.0
    assert "alpha = (span + 1) / 2.0" not in content, "The script still contains the buggy alpha calculation."