# test_final_state.py

import os
import csv
import pytest

def get_expected_values():
    data_file = "/home/user/etl_data.csv"
    assert os.path.exists(data_file), f"Input file {data_file} is missing."

    records = []
    with open(data_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    # Sort chronologically by timestamp
    records.sort(key=lambda x: x['timestamp'])

    # Deduplicate by record_id (keep first occurrence)
    seen_ids = set()
    deduped = []
    for r in records:
        if r['record_id'] not in seen_ids:
            seen_ids.add(r['record_id'])
            deduped.append(r)

    # Forward fill missing sensor_values and compute metrics
    total_sum = 0.0
    anomalies = 0
    last_val = None

    for r in deduped:
        val_str = r['sensor_value'].strip()
        if val_str:
            val = float(val_str)
            last_val = val
        else:
            val = last_val

        total_sum += val
        if val > 100.0:
            anomalies += 1

    avg = total_sum / len(deduped) if deduped else 0.0
    # Round to exactly two decimal places
    avg_rounded = f"{avg:.2f}"

    return avg_rounded, anomalies

def test_process_etl_script_exists_and_executable():
    script_path = "/home/user/process_etl.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_final_report_content():
    report_path = "/home/user/final_report.txt"
    assert os.path.exists(report_path), f"Final report {report_path} does not exist."

    avg_val, anomaly_count = get_expected_values()

    template_path = "/home/user/report_template.txt"
    assert os.path.exists(template_path), f"Template {template_path} is missing."

    with open(template_path, 'r') as f:
        template = f.read()

    expected_report = template.replace("{{AVG_VALUE}}", str(avg_val)).replace("{{ANOMALY_COUNT}}", str(anomaly_count))

    with open(report_path, 'r') as f:
        actual_report = f.read()

    assert actual_report.strip() == expected_report.strip(), (
        f"Content of {report_path} is incorrect.\n"
        f"Expected:\n{expected_report}\n"
        f"Got:\n{actual_report}"
    )