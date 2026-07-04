# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_first_10_frames_csv():
    csv_path = "/home/user/first_10_frames.csv"
    assert os.path.exists(csv_path), f"Missing output file: {csv_path}"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"CSV file {csv_path} is empty")

        assert header == ['frame_id', 'intensity', 'event_flag'], f"Incorrect header in {csv_path}: {header}"

        rows = list(reader)
        assert len(rows) == 10, f"Expected exactly 10 data rows, found {len(rows)}"

        for i, row in enumerate(rows):
            assert len(row) == 3, f"Row {i} has {len(row)} columns instead of 3"
            assert row[0] == str(i), f"Row {i}: Expected frame_id '{i}', got '{row[0]}'"
            try:
                intensity = float(row[1])
            except ValueError:
                pytest.fail(f"Row {i}: Intensity '{row[1]}' is not a valid float")

            assert 0.0 <= intensity <= 255.0, f"Row {i}: Intensity {intensity} is out of bounds [0.0, 255.0]"

            # Check if it has at most 2 decimal places (by checking string representation, though floats might have precision issues)
            # A simple check:
            if '.' in row[1]:
                decimals = len(row[1].split('.')[1])
                assert decimals <= 2 or round(intensity, 2) == intensity, f"Row {i}: Intensity '{row[1]}' not rounded to 2 decimal places"

            assert row[2] == "False", f"Row {i}: Expected event_flag 'False', got '{row[2]}'"

def test_validator_clean_corpus():
    script_path = "/home/user/validate_csv.py"
    assert os.path.exists(script_path), f"Missing validator script: {script_path}"

    clean_dir = "/app/clean_corpus/"
    assert os.path.exists(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No CSV files found in clean corpus"

    failed_files = []
    for cf in clean_files:
        res = subprocess.run(['python3', script_path, cf], capture_output=True)
        if res.returncode != 0:
            failed_files.append(os.path.basename(cf))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files rejected: {failed_files}"

def test_validator_evil_corpus():
    script_path = "/home/user/validate_csv.py"
    assert os.path.exists(script_path), f"Missing validator script: {script_path}"

    evil_dir = "/app/evil_corpus/"
    assert os.path.exists(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No CSV files found in evil corpus"

    bypassed_files = []
    for ef in evil_files:
        res = subprocess.run(['python3', script_path, ef], capture_output=True)
        if res.returncode == 0:
            bypassed_files.append(os.path.basename(ef))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed validation: {bypassed_files}"