# test_final_state.py
import os
import csv
import stat
import hashlib
import re

def test_pipeline_script_exists():
    assert os.path.isfile('/home/user/pipeline.py'), "pipeline.py is missing"

def test_run_pipeline_sh():
    sh_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(sh_path), "run_pipeline.sh is missing"
    st = os.stat(sh_path)
    assert bool(st.st_mode & stat.S_IXUSR), "run_pipeline.sh is not executable"

def test_cron_txt():
    cron_path = '/home/user/cron.txt'
    assert os.path.isfile(cron_path), "cron.txt is missing"
    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Match cron expression for 03:15 AM
    # Accept 15 3 * * * or 15 03 * * *
    match = re.search(r'^15\s+0?3\s+\*\s+\*\s+\*\s+/home/user/run_pipeline\.sh$', content)
    assert match is not None, f"cron.txt does not contain the correct cron schedule. Found: {content}"

def test_audit_sample_csv():
    csv_path = '/home/user/audit_sample.csv'
    assert os.path.isfile(csv_path), "audit_sample.csv is missing"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames is not None, "audit_sample.csv has no header"
    expected_columns = ['PatientID', 'PatientName', 'Condition', 'HeartRate', 'RollingHR']
    for col in expected_columns:
        assert col in reader.fieldnames, f"Column {col} missing in audit_sample.csv"

    # We expect exactly 2 rows (50% of 2 Cardiac = 1, 50% of 3 Resp = 1)
    assert len(rows) == 2, f"Expected 2 rows in audit_sample.csv, got {len(rows)}"

    # Check sorting by PatientID
    pids = [row['PatientID'] for row in rows]
    assert pids == sorted(pids), "audit_sample.csv is not sorted by PatientID in ascending order"

    # Precomputed expected values for the latest day (2023-10-03)
    expected_data = {
        'P01': {'Condition': 'Cardiac', 'HeartRate': 70.0, 'RollingHR': 72.66666666666667, 'Name': 'Alice Smith'},
        'P02': {'Condition': 'Cardiac', 'HeartRate': 81.0, 'RollingHR': 81.0, 'Name': 'Bob Jones'},
        'P03': {'Condition': 'Resp', 'HeartRate': 88.0, 'RollingHR': 89.33333333333333, 'Name': 'Carol White'},
        'P04': {'Condition': 'Resp', 'HeartRate': 86.0, 'RollingHR': 85.5, 'Name': 'David Brown'},
        'P05': {'Condition': 'Resp', 'HeartRate': 92.0, 'RollingHR': 94.0, 'Name': 'Eve Davis'},
    }

    conditions_seen = set()

    for row in rows:
        pid = row['PatientID']
        assert pid in expected_data, f"Unexpected PatientID {pid} in audit_sample.csv"

        expected = expected_data[pid]

        # Check Condition
        assert row['Condition'] == expected['Condition'], f"Incorrect Condition for {pid}"
        conditions_seen.add(row['Condition'])

        # Check Hash
        expected_hash = hashlib.sha256(expected['Name'].encode('utf-8')).hexdigest()[:8].lower()
        assert row['PatientName'] == expected_hash, f"Incorrect PatientName hash for {pid}. Expected {expected_hash}, got {row['PatientName']}"

        # Check HeartRate
        hr = float(row['HeartRate'])
        assert abs(hr - expected['HeartRate']) < 1e-5, f"Incorrect HeartRate for {pid}. Expected {expected['HeartRate']}, got {hr}"

        # Check RollingHR
        rhr = float(row['RollingHR'])
        assert abs(rhr - expected['RollingHR']) < 1e-5, f"Incorrect RollingHR for {pid}. Expected {expected['RollingHR']}, got {rhr}"

    assert 'Cardiac' in conditions_seen, "Missing Cardiac sample"
    assert 'Resp' in conditions_seen, "Missing Resp sample"