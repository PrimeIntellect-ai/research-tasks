# test_final_state.py
import os
import csv
import math
from datetime import datetime

def get_time_of_day(dt_str):
    # Parse ISO 8601 format, e.g., 2023-10-10T05:15:00Z
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
    hour = dt.hour
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Night"

def compute_expected_anomalies(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Sort chronologically
    rows.sort(key=lambda x: x['timestamp'])

    servers = {}
    anomalies = []

    for row in rows:
        srv = row['server_id']
        cpu = float(row['cpu_usage'])
        ts = row['timestamp']
        tod = get_time_of_day(ts)

        if srv not in servers:
            servers[srv] = []

        servers[srv].append(cpu)
        window = servers[srv][-4:]

        n = len(window)
        mean = sum(window) / n
        if n < 2:
            std = 0.0
        else:
            variance = sum((x - mean) ** 2 for x in window) / (n - 1)
            std = math.sqrt(variance)

        if cpu > mean + 1.5 * std and cpu > 80.0:
            anomalies.append({
                'timestamp': ts,
                'server_id': srv,
                'cpu_usage': round(cpu, 1),
                'time_of_day': tod
            })

    return anomalies

def test_anomaly_report_exists_and_correct():
    csv_path = "/home/user/data/metrics.csv"
    report_path = "/home/user/anomaly_report.md"

    assert os.path.exists(csv_path), f"Input data missing at {csv_path}"
    assert os.path.exists(report_path), f"Report missing at {report_path}"

    expected_anomalies = compute_expected_anomalies(csv_path)

    with open(report_path, 'r') as f:
        report_content = f.read()

    # Check total count
    expected_total_str = f"## Total Anomalies Detected: {len(expected_anomalies)}"
    assert expected_total_str in report_content, f"Report must contain the correct total anomalies count string: '{expected_total_str}'"

    # Check table headers
    assert "| Timestamp | Server ID | CPU Usage | Time of Day |" in report_content, "Report is missing the correct markdown table headers."
    assert "|-----------|-----------|-----------|-------------|" in report_content, "Report is missing the markdown table separator."

    # Check each anomaly row
    for anomaly in expected_anomalies:
        # Construct the expected row string ignoring exact spacing around pipes by checking parts or using a regex-like approach
        # A simple approach is to check if all parts are in the same line
        lines = report_content.split('\n')
        found = False
        for line in lines:
            if anomaly['timestamp'] in line and anomaly['server_id'] in line and str(anomaly['cpu_usage']) in line and anomaly['time_of_day'] in line:
                found = True
                break
        assert found, f"Expected anomaly not found in report: {anomaly}"

def test_script_exists():
    script_path = "/home/user/analyze_metrics.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."