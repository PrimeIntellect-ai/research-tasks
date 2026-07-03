# test_final_state.py
import os
import json
import sqlite3
import base64
import pytest

def get_expected_critical_tickets():
    db_path = '/home/user/ticket_system/tickets.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, payload FROM tickets ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    expected_ids = []
    for t_id, payload in rows:
        if payload.startswith("DATA:"):
            b64_part = payload[5:]
            try:
                decoded = base64.b64decode(b64_part, validate=True)
                data = json.loads(decoded.decode('utf-8'))
                if data.get("critical") is True:
                    expected_ids.append(t_id)
            except Exception:
                pass
    return expected_ids

def test_critical_tickets_json_exists_and_correct():
    json_path = '/home/user/ticket_system/critical_tickets.json'
    assert os.path.isfile(json_path), f"Output file {json_path} was not generated. Did the script run successfully?"

    with open(json_path, 'r') as f:
        try:
            actual_ids = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {json_path} is not valid JSON.")

    expected_ids = get_expected_critical_tickets()

    assert isinstance(actual_ids, list), "Output JSON should be a list of integers."

    # Check if they only got partial results (e.g. missing 11 and 22 due to pagination bug)
    if set(actual_ids) == {45} and expected_ids != actual_ids:
        pytest.fail("The output only contains ticket 45. The pagination bug (skipping records) is likely still present.")

    assert actual_ids == expected_ids, f"Expected critical ticket IDs {expected_ids}, but got {actual_ids}. Both slicing and pagination bugs must be fixed."