# test_final_state.py
import os
import re
import json
import hashlib
import subprocess
import pandas as pd
from datetime import datetime, timedelta
import pytest
from sklearn.metrics import mean_squared_error

def generate_ground_truth():
    cmd = ["/app/log_emitter"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    pattern = re.compile(r'^\[(.*?)\]\s+(\S+)\s+(\S+).*?bytes=(\d+)')

    seen_hashes = set()
    user_windows = {}
    user_counts = {}

    results = []

    for line in process.stdout:
        match = pattern.search(line)
        if not match:
            continue

        timestamp_str, user_id, action, bytes_str = match.groups()

        try:
            dt = datetime.fromisoformat(timestamp_str)
        except ValueError:
            continue

        bytes_val = int(bytes_str)

        # Deduplication
        hash_input = f"{timestamp_str}{user_id}{action}".encode('utf-8')
        md5_hash = hashlib.md5(hash_input).hexdigest()

        if md5_hash in seen_hashes:
            continue
        seen_hashes.add(md5_hash)

        # Windowed Rolling Aggregation
        if user_id not in user_windows:
            user_windows[user_id] = []
            user_counts[user_id] = 0

        window = user_windows[user_id]
        window.append((dt, bytes_val))

        # Remove old entries
        cutoff_time = dt - timedelta(minutes=5)
        while window and window[0][0] < cutoff_time:
            window.pop(0)

        avg_bytes = sum(b for _, b in window) / len(window)

        # Stratification (1st, 11th, 21st...)
        if user_counts[user_id] % 10 == 0:
            results.append({
                'timestamp': timestamp_str,
                'user_id': user_id,
                'action': action,
                'bytes': bytes_val,
                'rolling_avg_bytes': avg_bytes
            })

        user_counts[user_id] += 1

    process.wait()
    return pd.DataFrame(results)

def test_pipeline_results():
    agent_csv_path = "/home/user/rolling_averages.csv"
    assert os.path.exists(agent_csv_path), f"Agent output missing at {agent_csv_path}"

    agent_df = pd.read_csv(agent_csv_path)
    assert not agent_df.empty, "Agent CSV is empty"

    required_columns = ['timestamp', 'user_id', 'action', 'bytes', 'rolling_avg_bytes']
    for col in required_columns:
        assert col in agent_df.columns, f"Missing column {col} in agent CSV"

    gt_df = generate_ground_truth()

    # Merge to compare
    merged = pd.merge(gt_df, agent_df, on=['timestamp', 'user_id'], suffixes=('_gt', '_agent'), how='inner')

    assert len(merged) > 0, "No matching rows found between agent output and ground truth."

    # Check if agent missed too many rows
    coverage = len(merged) / len(gt_df)
    assert coverage >= 0.95, f"Agent output is missing too many rows. Coverage: {coverage:.2%}"

    mse = mean_squared_error(merged['rolling_avg_bytes_gt'], merged['rolling_avg_bytes_agent'])

    assert mse <= 0.01, f"MSE {mse:.4f} exceeds threshold of 0.01"

def test_metrics_json():
    metrics_path = "/home/user/pipeline_metrics.json"
    assert os.path.exists(metrics_path), f"Metrics JSON missing at {metrics_path}"

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("pipeline_metrics.json is not valid JSON")

    assert "total_lines_read" in metrics, "Missing 'total_lines_read' in metrics"
    assert "valid_parsed_lines" in metrics, "Missing 'valid_parsed_lines' in metrics"
    assert "deduplicated_lines" in metrics, "Missing 'deduplicated_lines' in metrics"