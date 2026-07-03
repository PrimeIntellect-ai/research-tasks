# test_final_state.py
import os
import json
import pytest

def test_attacker_ip_file():
    ip_file = "/home/user/attacker_ip.txt"
    assert os.path.isfile(ip_file), f"File {ip_file} does not exist. Did you write the extracted IP to this location?"

    with open(ip_file, 'r') as f:
        ip = f.read().strip()

    assert ip == "192.168.137.42", f"Expected IP '192.168.137.42', got '{ip}'. The wrong IP was extracted."

def test_recovered_db_json():
    json_file = "/home/user/incident/recovered_db.json"
    assert os.path.isfile(json_file), f"File {json_file} does not exist. Did you run the fixed recover.py script?"

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_file} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {json_file}, got {type(data).__name__}."
    assert len(data) == 3, f"Expected 3 records in {json_file}, got {len(data)}. The off-by-one error might not be fully fixed."
    assert data[-1].get("action") == "SYSTEM_CRASH", "The last record is missing or incorrect. It should be the SYSTEM_CRASH event."