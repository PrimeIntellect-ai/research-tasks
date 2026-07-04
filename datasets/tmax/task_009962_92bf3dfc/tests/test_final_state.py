# test_final_state.py
import os
import json
import math
import subprocess
import pytest

def compute_expected_alerts(data_dir):
    expected = {}
    for filename in os.listdir(data_dir):
        if not filename.endswith('.csv'):
            continue
        server_name = filename[:-4]
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'r') as f:
            lines = f.read().strip().split('\n')

        if len(lines) <= 1:
            expected[server_name] = []
            continue

        data = []
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split(',')
            data.append((int(parts[0]), float(parts[1])))

        if len(data) < 3:
            expected[server_name] = []
            continue

        rolling_avgs = []
        valid_ts = []
        for i in range(2, len(data)):
            avg = (data[i][1] + data[i-1][1] + data[i-2][1]) / 3.0
            rolling_avgs.append(avg)
            valid_ts.append(data[i][0])

        if not rolling_avgs:
            expected[server_name] = []
            continue

        mean = sum(rolling_avgs) / len(rolling_avgs)
        variance = sum((x - mean) ** 2 for x in rolling_avgs) / len(rolling_avgs)
        std = math.sqrt(variance)

        alerts = []
        if std > 0:
            for t, ra in zip(valid_ts, rolling_avgs):
                z = (ra - mean) / std
                if z > 1.5:
                    alerts.append({"timestamp": t, "z_score": round(z, 3)})

        expected[server_name] = alerts

    return expected

def test_pipeline_execution():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_alerts_json_output():
    json_path = "/home/user/alerts.json"
    assert os.path.isfile(json_path), f"Output file {json_path} was not created."

    with open(json_path, 'r') as f:
        try:
            actual_alerts = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    data_dir = "/home/user/drift_data"
    expected_alerts = compute_expected_alerts(data_dir)

    # Check that all expected servers are in the output
    for server, alerts in expected_alerts.items():
        assert server in actual_alerts, f"Server '{server}' missing from output JSON."

        # Sort both expected and actual alerts by timestamp for comparison
        expected_sorted = sorted(alerts, key=lambda x: x["timestamp"])
        actual_sorted = sorted(actual_alerts[server], key=lambda x: x["timestamp"])

        assert len(actual_sorted) == len(expected_sorted), f"Alert count mismatch for server '{server}'. Expected {len(expected_sorted)}, got {len(actual_sorted)}."

        for exp, act in zip(expected_sorted, actual_sorted):
            assert exp["timestamp"] == act["timestamp"], f"Timestamp mismatch for server '{server}'. Expected {exp['timestamp']}, got {act['timestamp']}."
            assert math.isclose(exp["z_score"], act["z_score"], abs_tol=0.002), f"Z-score mismatch for server '{server}' at timestamp {exp['timestamp']}. Expected {exp['z_score']}, got {act['z_score']}."

    # Check if there are any extra servers in the output
    for server in actual_alerts:
        assert server in expected_alerts, f"Unexpected server '{server}' found in output JSON."