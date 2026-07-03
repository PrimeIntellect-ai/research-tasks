# test_final_state.py

import os
import csv
import stat
import subprocess
import pytest
from itertools import combinations

RAW_DIR = "/home/user/configs/raw"
REPORT_FILE = "/home/user/reports/anomalies.csv"
SCRIPT_FILE = "/home/user/run_pipeline.sh"

def parse_ini(filepath):
    config = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip().lower()
                val = val.strip()
                config[key] = val
    return set(f"{k}={v}" for k, v in config.items())

def compute_expected_anomalies():
    if not os.path.exists(RAW_DIR):
        return []

    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.ini')]
    parsed_configs = {}
    for fname in files:
        parsed_configs[fname] = parse_ini(os.path.join(RAW_DIR, fname))

    anomalies = []
    for f1, f2 in combinations(sorted(files), 2):
        set1 = parsed_configs[f1]
        set2 = parsed_configs[f2]

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        if union == 0:
            sim = 0.0
        else:
            sim = intersection / union

        if sim < 0.35:
            anomalies.append((f1, f2, f"{sim:.4f}"))

    # Sort alphabetically by file1, then file2
    anomalies.sort(key=lambda x: (x[0], x[1]))
    return anomalies

def test_anomalies_csv_exists():
    assert os.path.isfile(REPORT_FILE), f"The anomalies report was not found at {REPORT_FILE}"

def test_anomalies_csv_content():
    assert os.path.isfile(REPORT_FILE), f"Missing {REPORT_FILE}"

    expected_anomalies = compute_expected_anomalies()

    with open(REPORT_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"The file {REPORT_FILE} is empty"
    assert rows[0] == ['file1', 'file2', 'similarity'], f"Incorrect header in {REPORT_FILE}. Expected ['file1', 'file2', 'similarity'], got {rows[0]}"

    actual_anomalies = [tuple(row) for row in rows[1:]]

    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalous pairs, but found {len(actual_anomalies)} in {REPORT_FILE}"

    for expected, actual in zip(expected_anomalies, actual_anomalies):
        assert expected == actual, f"Mismatch in CSV row. Expected {expected}, got {actual}"

def test_pipeline_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_FILE), f"Pipeline script not found at {SCRIPT_FILE}"
    st = os.stat(SCRIPT_FILE)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {SCRIPT_FILE} is not executable"

def test_crontab_scheduled():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure a crontab is set up for the user.")

    cron_lines = [line.strip() for line in output.splitlines() if line.strip() and not line.strip().startswith('#')]

    found = False
    for line in cron_lines:
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "* * * * *" and SCRIPT_FILE in command:
                found = True
                break

    assert found, f"Could not find a crontab entry running {SCRIPT_FILE} every minute (* * * * *)"