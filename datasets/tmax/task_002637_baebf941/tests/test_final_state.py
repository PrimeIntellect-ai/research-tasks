# test_final_state.py
import csv
import json
import subprocess
import math
from collections import defaultdict
import os

def test_anomalies_csv_mse():
    # Re-derive Ground Truth
    try:
        output = subprocess.check_output(["/app/log_emitter"], text=True)
    except Exception as e:
        assert False, f"Failed to run /app/log_emitter: {e}"

    buckets = defaultdict(lambda: {'ips': set(), 'login': 0, 'data': 0, 'health': 0})

    for line in output.strip().split('\n'):
        # Clean bad unicode escapes
        cleaned = line.replace('\\uXX12', '') 
        try:
            data = json.loads(cleaned)
            ts = data['timestamp']
            b_start = (ts // 60) * 60

            # Mask IP
            ip_parts = data['client_ip'].split('.')
            ip_parts[3] = '0'
            masked_ip = '.'.join(ip_parts)

            buckets[b_start]['ips'].add(masked_ip)
            ep = data['endpoint']
            if ep == '/login': buckets[b_start]['login'] += 1
            elif ep == '/data': buckets[b_start]['data'] += 1
            elif ep == '/health': buckets[b_start]['health'] += 1
        except:
            pass

    truth_distances = {}
    for b_start, b_data in buckets.items():
        v1 = [b_data['login'], b_data['data'], b_data['health']]
        v2 = [15, 45, 10]
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
        truth_distances[str(b_start)] = dist

    agent_file = "/home/user/anomalies.csv"
    assert os.path.exists(agent_file), f"Agent output file not found at {agent_file}"

    mse = 0.0
    count = 0

    try:
        with open(agent_file, 'r') as f:
            reader = csv.DictReader(f)
            assert 'bucket_start_timestamp' in reader.fieldnames and 'distance' in reader.fieldnames, \
                "CSV missing required columns 'bucket_start_timestamp' or 'distance'"
            for row in reader:
                b_ts = row.get('bucket_start_timestamp')
                if b_ts in truth_distances:
                    agent_dist = float(row['distance'])
                    mse += (agent_dist - truth_distances[b_ts]) ** 2
                    count += 1
    except Exception as e:
        assert False, f"Error reading agent output {agent_file}: {e}"

    assert count > 0, "No matching buckets found in agent output."

    mse /= count

    expected_min_count = len(truth_distances) * 0.9
    assert count >= expected_min_count, f"Agent output has {count} matching buckets, expected at least {expected_min_count}"
    assert mse <= 0.01, f"MSE {mse:.6f} exceeds threshold 0.01"