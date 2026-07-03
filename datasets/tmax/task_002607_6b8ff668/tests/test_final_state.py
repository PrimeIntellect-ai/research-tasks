# test_final_state.py

import os
import json
import csv
import time
import subprocess
from datetime import datetime, timezone

def compute_hash(config_val: str) -> str:
    h = 0x5A5A5A5A
    for c in config_val:
        h = ((h * 33) ^ ord(c)) & 0xFFFFFFFF
    return f"{h:08x}"

def generate_golden_output():
    records = []

    # Read CSV
    csv_path = "/home/user/data/configs.csv"
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                records.append({
                    "timestamp": dt,
                    "server": row["server_id"],
                    "val": row["config_val"]
                })

    # Read JSON
    json_path = "/home/user/data/configs.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                dt = datetime.fromtimestamp(item["time"], tz=timezone.utc)
                records.append({
                    "timestamp": dt,
                    "server": item["server"],
                    "val": item["val"]
                })

    # Sort by timestamp to keep earliest during deduplication
    records.sort(key=lambda x: x["timestamp"])

    buckets = {}
    for r in records:
        bucket_dt = r["timestamp"].replace(minute=0, second=0, microsecond=0)
        bucket_str = bucket_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        if bucket_str not in buckets:
            buckets[bucket_str] = {}

        dedup_key = (r["server"], r["val"])
        if dedup_key not in buckets[bucket_str]:
            buckets[bucket_str][dedup_key] = r["val"]

    aggregated = {}
    for bucket_str, items in buckets.items():
        hashes = [compute_hash(val) for val in items.values()]
        aggregated[bucket_str] = sorted(hashes)

    return aggregated

def test_output_correctness():
    output_path = "/home/user/output/aggregated.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r", encoding="utf-8") as f:
        try:
            student_output = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    golden_output = generate_golden_output()

    assert student_output == golden_output, "The aggregated JSON output does not match the expected golden output."

def test_performance():
    script_path = "/home/user/process.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    start_time = time.perf_counter()
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    end_time = time.perf_counter()

    assert result.returncode == 0, f"Script failed to execute. Stderr: {result.stderr}"

    execution_time = end_time - start_time
    threshold = 5.0

    assert execution_time <= threshold, (
        f"Performance check failed: Execution took {execution_time:.2f} seconds, "
        f"which exceeds the maximum allowed time of {threshold} seconds. "
        "Make sure to reverse-engineer the hashing binary and implement it natively in Python."
    )