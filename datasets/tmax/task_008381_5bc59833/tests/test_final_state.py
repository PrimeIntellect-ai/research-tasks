# test_final_state.py

import os
from datetime import datetime, timezone

def test_script_exists_and_executable():
    script_path = '/home/user/analyze_logs.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_anomaly_report_exists():
    report_path = '/home/user/anomaly_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

def compute_expected_anomaly():
    log_a_path = '/home/user/logs/server_A.log'
    log_b_path = '/home/user/logs/server_B.log'

    records = set()

    if os.path.exists(log_a_path):
        with open(log_a_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    records.add(line)

    if os.path.exists(log_b_path):
        with open(log_b_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 5:
                        ts, ip, status, resp_time, payload = parts
                        dt = datetime.fromtimestamp(int(ts), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                        normalized_line = f"{dt}|{ip}|{status}|{resp_time}|{payload}"
                        records.add(normalized_line)

    minutes_data = {}
    for record in records:
        parts = record.split('|')
        if len(parts) == 5:
            dt, ip, status, resp_time, payload = parts
            minute = dt[:16] # Extract YYYY-MM-DD HH:MM
            status = int(status)
            resp_time = int(resp_time)

            if minute not in minutes_data:
                minutes_data[minute] = {'errors': 0, 'resp_times': []}

            if status >= 500:
                minutes_data[minute]['errors'] += 1
            minutes_data[minute]['resp_times'].append(resp_time)

    sorted_minutes = sorted(minutes_data.keys())
    for minute in sorted_minutes:
        data = minutes_data[minute]
        errors = data['errors']
        avg_time = sum(data['resp_times']) // len(data['resp_times'])

        if errors > 3 and avg_time > 1000:
            return f"ANOMALY_MINUTE: {minute}, ERRORS: {errors}, AVG_TIME: {avg_time}ms"

    return None

def test_anomaly_report_content():
    report_path = '/home/user/anomaly_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        actual_content = f.read().strip()

    expected_content = compute_expected_anomaly()

    assert expected_content is not None, "Could not compute expected anomaly from logs. Logs might be missing or corrupted."
    assert actual_content == expected_content, f"Report content is incorrect.\nExpected: '{expected_content}'\nActual: '{actual_content}'"