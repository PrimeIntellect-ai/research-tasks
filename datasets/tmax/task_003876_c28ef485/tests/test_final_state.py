# test_final_state.py

import os
import csv
import pytest

def get_expected_results(csv_path):
    expected_sample = [["id", "region", "status", "amount"]]
    failed_count = 0
    success_sum = 0
    region_counts = {}

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row['status']
            if status == 'FAILED':
                failed_count += 1
            elif status == 'SUCCESS':
                success_sum += int(row['amount'])
                region = row['region']
                region_counts[region] = region_counts.get(region, 0) + 1
                if region_counts[region] <= 3:
                    expected_sample.append([row['id'], row['region'], row['status'], row['amount']])

    return expected_sample, failed_count, success_sum

def test_script_exists_and_executable():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_failed_count():
    csv_path = "/home/user/data/events.csv"
    _, expected_failed_count, _ = get_expected_results(csv_path)

    out_path = "/home/user/output/failed_count.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    with open(out_path, 'r') as f:
        content = f.read().strip()

    assert content == str(expected_failed_count), f"Expected failed count {expected_failed_count}, got {content}."

def test_success_sum():
    csv_path = "/home/user/data/events.csv"
    _, _, expected_success_sum = get_expected_results(csv_path)

    out_path = "/home/user/output/success_sum.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    with open(out_path, 'r') as f:
        content = f.read().strip()

    assert content == str(expected_success_sum), f"Expected success sum {expected_success_sum}, got {content}."

def test_sample_csv():
    csv_path = "/home/user/data/events.csv"
    expected_sample, _, _ = get_expected_results(csv_path)

    out_path = "/home/user/output/sample.csv"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    actual_sample = []
    with open(out_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_sample.append(row)

    assert actual_sample == expected_sample, f"Expected sample CSV content {expected_sample}, got {actual_sample}."