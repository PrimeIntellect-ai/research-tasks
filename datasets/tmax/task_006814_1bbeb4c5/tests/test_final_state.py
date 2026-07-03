# test_final_state.py

import os
import json
import csv
import math
import pytest

def compute_expected_output(input_file):
    groups = {}
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            timestamp = int(row['timestamp'])
            server_id = row['server_id']
            cpu_usage = float(row['cpu_usage'])
            memory_bytes = int(row['memory_bytes'])

            bucket = timestamp - (timestamp % 300)
            key = (bucket, server_id)

            if key not in groups:
                groups[key] = {
                    'cpu_usages': [],
                    'max_memory': -1,
                    'spike_count': 0
                }

            groups[key]['cpu_usages'].append(cpu_usage)
            if memory_bytes > groups[key]['max_memory']:
                groups[key]['max_memory'] = memory_bytes
            if cpu_usage > 90.0:
                groups[key]['spike_count'] += 1

    expected_output = []
    for key in sorted(groups.keys()):
        bucket, server_id = key
        data = groups[key]
        avg_cpu = sum(data['cpu_usages']) / len(data['cpu_usages'])
        max_mem_norm = data['max_memory'] / 32000000000.0

        expected_output.append({
            "bucket": bucket,
            "server_id": server_id,
            "avg_cpu": avg_cpu,
            "max_mem_norm": max_mem_norm,
            "spike_count": data['spike_count']
        })

    return expected_output

def test_etl_output_exists_and_correct():
    input_file = "/home/user/raw_metrics.csv"
    output_file = "/home/user/etl_output.jsonl"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist. Did you run your ETL pipeline?"
    assert os.path.isfile(output_file), f"{output_file} is not a valid file."

    expected_data = compute_expected_output(input_file)

    actual_data = []
    with open(output_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_data.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {output_file} is not a valid JSON object.")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert "bucket" in actual, f"Record {i} missing 'bucket' key."
        assert "server_id" in actual, f"Record {i} missing 'server_id' key."
        assert "avg_cpu" in actual, f"Record {i} missing 'avg_cpu' key."
        assert "max_mem_norm" in actual, f"Record {i} missing 'max_mem_norm' key."
        assert "spike_count" in actual, f"Record {i} missing 'spike_count' key."

        assert actual["bucket"] == expected["bucket"], f"Record {i} bucket mismatch: expected {expected['bucket']}, got {actual['bucket']}."
        assert actual["server_id"] == expected["server_id"], f"Record {i} server_id mismatch: expected {expected['server_id']}, got {actual['server_id']}."
        assert actual["spike_count"] == expected["spike_count"], f"Record {i} spike_count mismatch: expected {expected['spike_count']}, got {actual['spike_count']}."

        assert math.isclose(actual["avg_cpu"], expected["avg_cpu"], rel_tol=1e-4, abs_tol=1e-4), \
            f"Record {i} avg_cpu mismatch: expected {expected['avg_cpu']}, got {actual['avg_cpu']}."
        assert math.isclose(actual["max_mem_norm"], expected["max_mem_norm"], rel_tol=1e-4, abs_tol=1e-4), \
            f"Record {i} max_mem_norm mismatch: expected {expected['max_mem_norm']}, got {actual['max_mem_norm']}."