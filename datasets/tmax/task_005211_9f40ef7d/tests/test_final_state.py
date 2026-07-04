# test_final_state.py

import os
import json
from datetime import datetime, timezone

def parse_timestamp(ts):
    if isinstance(ts, int) or (isinstance(ts, str) and ts.isdigit()):
        return datetime.fromtimestamp(int(ts), tz=timezone.utc)
    else:
        # Handle ISO8601 string like "2023-10-01T15:30:00Z"
        return datetime.strptime(ts.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")

def compute_expected_summary(log_file):
    if not os.path.exists(log_file):
        return {}

    # service -> hour -> (timestamp, allocation)
    service_changes = {}

    with open(log_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            alloc = entry.get("allocation")

            # 1. Validation Gate
            if alloc is None or alloc < 0 or alloc > 10000:
                continue

            ts_raw = entry.get("timestamp")
            dt = parse_timestamp(ts_raw)

            # 2. Time Alignment (only 2023-10-01)
            if dt.year == 2023 and dt.month == 10 and dt.day == 1:
                service = entry.get("service")
                hour = dt.hour

                if service not in service_changes:
                    service_changes[service] = {}

                # Keep latest chronologically occurring allocation
                if hour not in service_changes[service]:
                    service_changes[service][hour] = (dt, alloc)
                else:
                    if dt > service_changes[service][hour][0]:
                        service_changes[service][hour] = (dt, alloc)

    summary = {}
    for service, hours in service_changes.items():
        buckets = []
        current_alloc = 0
        for h in range(24):
            if h in hours:
                current_alloc = hours[h][1]
            buckets.append(current_alloc)

        summary[service] = {
            "min": min(buckets),
            "max": max(buckets),
            "avg": round(sum(buckets) / 24, 2)
        }

    return summary

def test_summary_json_exists():
    summary_path = '/home/user/summary.json'
    assert os.path.exists(summary_path), f"The file {summary_path} is missing."
    assert os.path.isfile(summary_path), f"The path {summary_path} is not a file."

def test_summary_json_content():
    summary_path = '/home/user/summary.json'
    log_path = '/home/user/config_changes.jsonl'

    assert os.path.exists(summary_path), f"{summary_path} does not exist."
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_path} is not a valid JSON file."

    expected_summary = compute_expected_summary(log_path)

    # Check that the keys match exactly
    assert set(actual_summary.keys()) == set(expected_summary.keys()), \
        f"Expected services {list(expected_summary.keys())}, but got {list(actual_summary.keys())}."

    for service, expected_stats in expected_summary.items():
        actual_stats = actual_summary[service]

        assert actual_stats.get("min") == expected_stats["min"], \
            f"Service '{service}': expected min {expected_stats['min']}, got {actual_stats.get('min')}"

        assert actual_stats.get("max") == expected_stats["max"], \
            f"Service '{service}': expected max {expected_stats['max']}, got {actual_stats.get('max')}"

        # Float comparison for average
        expected_avg = expected_stats["avg"]
        actual_avg = actual_stats.get("avg")
        assert actual_avg is not None, f"Service '{service}': missing 'avg' key"
        assert abs(actual_avg - expected_avg) <= 0.01, \
            f"Service '{service}': expected avg {expected_avg}, got {actual_avg}"