# test_final_state.py

import os
import re
import csv
import pytest

def test_workflow_script_properties():
    script_path = "/home/user/workflow.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "xargs" in content or "parallel" in content, (
        "The script must use parallel processing (e.g., xargs or parallel)."
    )

def process_expected_data(input_path):
    expected_rows = []
    with open(input_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        expected_rows.append(reader.fieldnames)

        for row in reader:
            # 1. Constraint-based Validation & Regex
            if not re.match(r'^\d{3}-\d{2}-\d{4}$', row['SSN']):
                continue

            try:
                age = int(row['Age'])
                if not (0 <= age <= 120):
                    continue
            except ValueError:
                continue

            # 2. Data Masking and Anonymization
            row['Name'] = 'REDACTED'
            row['SSN'] = f"***-**-{row['SSN'][-4:]}"

            # 3. Interpolation and Imputation
            if not row['BloodPressure'].strip():
                row['BloodPressure'] = '120/80'
            if not row['HeartRate'].strip():
                row['HeartRate'] = '72'

            expected_rows.append([row[field] for field in reader.fieldnames])

    return expected_rows

def test_processed_data_batch1():
    input_file = "/home/user/raw_data/batch1.csv"
    output_file = "/home/user/processed_data/batch1.csv"

    assert os.path.isfile(output_file), f"Processed file {output_file} is missing."

    expected_data = process_expected_data(input_file)

    with open(output_file, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert actual_data == expected_data, f"Data in {output_file} does not match the expected processed output."

def test_processed_data_batch2():
    input_file = "/home/user/raw_data/batch2.csv"
    output_file = "/home/user/processed_data/batch2.csv"

    assert os.path.isfile(output_file), f"Processed file {output_file} is missing."

    expected_data = process_expected_data(input_file)

    with open(output_file, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert actual_data == expected_data, f"Data in {output_file} does not match the expected processed output."