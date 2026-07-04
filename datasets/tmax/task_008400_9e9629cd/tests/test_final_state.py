# test_final_state.py

import os
import json
import hashlib
import pytest

def compute_expected_anomalies(input_file):
    if not os.path.isfile(input_file):
        pytest.fail(f"Input file {input_file} is missing.")

    seen_hashes = set()
    deduplicated_records = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            raw_string = line.rstrip('\n')
            if not raw_string:
                continue

            line_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
            if line_hash in seen_hashes:
                continue
            seen_hashes.add(line_hash)

            parts = raw_string.split('\t')
            if len(parts) >= 3:
                timestamp = parts[0]
                device_id = parts[1]
                payload_str = '\t'.join(parts[2:])
                try:
                    payload = json.loads(payload_str)
                    temperature = float(payload.get('temperature', 0.0))
                    deduplicated_records.append((timestamp, device_id, temperature))
                except json.JSONDecodeError:
                    pass

    # Group by device_id
    devices = {}
    for ts, dev, temp in deduplicated_records:
        if dev not in devices:
            devices[dev] = []
        devices[dev].append((ts, temp))

    expected_anomalies = {}
    for dev, records in devices.items():
        # Sort chronologically by timestamp
        records.sort(key=lambda x: x[0])

        for i in range(3, len(records)):
            prev_3 = records[i-3:i]
            mean_temp = sum(r[1] for r in prev_3) / 3.0
            current_temp = records[i][1]
            if current_temp - mean_temp >= 10.0:
                expected_anomalies[dev] = records[i][0]
                break

    return expected_anomalies

def test_anomalies_json_exists():
    """Check if the output JSON file is generated."""
    output_path = "/home/user/anomalies.json"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

def test_anomalies_json_content():
    """Check if the output JSON file contains the correct anomalies based on the input data."""
    output_path = "/home/user/anomalies.json"
    input_path = "/home/user/input/readings.tsv"

    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    with open(output_path, 'r', encoding='utf-8') as f:
        try:
            actual_anomalies = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    expected_anomalies = compute_expected_anomalies(input_path)

    assert actual_anomalies == expected_anomalies, (
        f"The anomalies in {output_path} do not match the expected results.\n"
        f"Expected: {expected_anomalies}\n"
        f"Actual: {actual_anomalies}"
    )

def test_script_exists():
    """Check if the process_pipeline.py script was created."""
    script_path = "/home/user/process_pipeline.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."