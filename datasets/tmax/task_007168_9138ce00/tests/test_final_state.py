# test_final_state.py

import os
import json
import subprocess
import pytest

def test_anomalies_file_exists():
    assert os.path.isfile('/home/user/output/anomalies.jsonl'), "Output file /home/user/output/anomalies.jsonl does not exist."

def test_anomalies_content():
    file_path = '/home/user/output/anomalies.jsonl'
    anomalies = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    anomalies.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Line in {file_path} is not valid JSON: {line}")

    assert len(anomalies) == 2, f"Expected exactly 2 anomalous records, found {len(anomalies)}."

    tx4 = next((a for a in anomalies if a.get('tx_id') == 'tx4'), None)
    assert tx4 is not None, "Expected anomaly 'tx4' is missing from the output."
    assert tx4.get('user_id') == 1, "tx4 user_id is incorrect."
    assert tx4.get('masked_ssn') == 'XXX-XX-3333', "tx4 masked_ssn is incorrect."
    assert tx4.get('masked_email') == 'a***@example.com', "tx4 masked_email is incorrect."
    assert tx4.get('amount') == 5000, "tx4 amount is incorrect."
    assert tx4.get('tokens') == ['luxury', 'watch', 'purchase'], "tx4 tokens are incorrect."

    # Ensure forbidden keys are absent
    forbidden_keys = {'ssn', 'email', 'description'}
    assert not forbidden_keys.intersection(tx4.keys()), "Output JSON objects must not contain original ssn, email, or description."

    tx8 = next((a for a in anomalies if a.get('tx_id') == 'tx8'), None)
    assert tx8 is not None, "Expected anomaly 'tx8' is missing from the output."
    assert tx8.get('user_id') == 2, "tx8 user_id is incorrect."
    assert tx8.get('masked_ssn') == 'XXX-XX-6666', "tx8 masked_ssn is incorrect."
    assert tx8.get('masked_email') == 'b***@test.org', "tx8 masked_email is incorrect."
    assert tx8.get('amount') == 200, "tx8 amount is incorrect."
    assert tx8.get('tokens') == ['fancy', 'dinner', 'at', '8pm'], "tx8 tokens are incorrect."
    assert not forbidden_keys.intersection(tx8.keys()), "Output JSON objects must not contain original ssn, email, or description."

def test_cron_configuration():
    assert os.path.isfile('/home/user/crontab.bak'), "/home/user/crontab.bak backup file is missing."

    try:
        crontab_out = subprocess.check_output(['crontab', '-u', 'user', '-l'], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab for 'user'. Ensure the crontab was installed correctly.")

    has_schedule = '*/15 * * * *' in crontab_out or '0,15,30,45 * * * *' in crontab_out
    has_script = 'etl.py' in crontab_out

    assert has_schedule, "Crontab does not contain the correct schedule (every 15 minutes)."
    assert has_script, "Crontab does not contain a reference to 'etl.py'."