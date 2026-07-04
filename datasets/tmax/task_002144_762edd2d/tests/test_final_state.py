# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_recovery_rate():
    payloads_file = '/app/data/payloads.jsonl'
    db_file = '/app/data/processed.db'

    assert os.path.isfile(payloads_file), f"Payloads file missing at {payloads_file}"

    # Calculate total valid payloads
    total_valid = 0
    try:
        with open(payloads_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                if data.get('is_corrupted') != True:
                    total_valid += 1
    except Exception as e:
        pytest.fail(f"Failed to read or parse payloads file: {e}")

    assert total_valid > 0, "No valid payloads found in the source file."

    # Calculate processed payloads
    processed = 0
    if os.path.isfile(db_file):
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM logs")
            row = cursor.fetchone()
            if row:
                processed = row[0]
            conn.close()
        except Exception as e:
            pytest.fail(f"Failed to query the processed database: {e}")
    else:
        pytest.fail(f"Processed database missing at {db_file}. Pipeline did not save data.")

    recovery_rate = processed / total_valid

    assert recovery_rate >= 0.98, (
        f"Data recovery rate is too low. "
        f"Processed {processed} out of {total_valid} valid payloads. "
        f"Recovery rate: {recovery_rate:.4f} (Threshold: 0.98)"
    )