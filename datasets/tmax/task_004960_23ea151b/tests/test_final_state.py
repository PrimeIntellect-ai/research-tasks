# test_final_state.py
import os
import re
import csv
from collections import defaultdict

def parse_logs(file_path):
    valid_logs = []
    pattern = re.compile(
        r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (DEVICE_[A-Za-z0-9]+) - STATUS:(\d{3}) - TIME:(\d+)ms - MSG:(.*)$"
    )

    with open(file_path, "r") as f:
        for original_index, line in enumerate(f):
            line = line.strip("\n")
            match = pattern.match(line)
            if match:
                timestamp, device_id, status_code, response_time, msg = match.groups()
                response_time = int(response_time)
                if response_time >= 0:
                    valid_logs.append({
                        "original_index": original_index,
                        "line": line,
                        "device_id": device_id,
                        "response_time": response_time
                    })
    return valid_logs

def test_final_state():
    raw_logs_path = "/home/user/raw_logs.txt"
    stats_path = "/home/user/device_stats.csv"
    sampled_path = "/home/user/sampled_logs.txt"

    assert os.path.exists(stats_path), f"Expected file {stats_path} does not exist."
    assert os.path.exists(sampled_path), f"Expected file {sampled_path} does not exist."

    valid_logs = parse_logs(raw_logs_path)

    # Compute expected stats
    device_times = defaultdict(list)
    for log in valid_logs:
        device_times[log["device_id"]].append(log["response_time"])

    expected_stats = []
    for device_id in sorted(device_times.keys()):
        times = device_times[device_id]
        mean_time = sum(times) / len(times)
        expected_stats.append((device_id, str(len(times)), f"{mean_time:.2f}"))

    # Read actual stats
    actual_stats = []
    with open(stats_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ["device_id", "log_count", "mean_response_time_ms"], f"Incorrect CSV headers in {stats_path}."
        for row in reader:
            actual_stats.append(tuple(row))

    assert actual_stats == expected_stats, f"Content of {stats_path} does not match expected stats."

    # Compute expected sampled logs
    device_logs = defaultdict(list)
    for log in valid_logs:
        device_logs[log["device_id"]].append(log)

    expected_sampled_lines = []
    for device_id in sorted(device_logs.keys()):
        logs = device_logs[device_id]
        # Sort by response_time (asc), then original_index (asc)
        logs.sort(key=lambda x: (x["response_time"], x["original_index"]))
        sampled = logs[:2]
        for log in sampled:
            expected_sampled_lines.append(log["line"])

    # Read actual sampled logs
    with open(sampled_path, "r") as f:
        actual_sampled_lines = [line.strip("\n") for line in f]

    assert actual_sampled_lines == expected_sampled_lines, f"Content of {sampled_path} does not match expected sampled logs."