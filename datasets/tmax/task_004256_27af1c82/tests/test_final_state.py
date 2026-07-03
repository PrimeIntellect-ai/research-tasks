# test_final_state.py
import os
import subprocess
import csv
import pytest
from pathlib import Path

def test_telemetry_filter_executable():
    filter_path = '/home/user/telemetry_filter'
    assert os.path.isfile(filter_path), f"Executable not found at {filter_path}"
    assert os.access(filter_path, os.X_OK), f"File at {filter_path} is not executable"

def run_filter(input_content):
    filter_path = '/home/user/telemetry_filter'
    process = subprocess.run(
        [filter_path],
        input=input_content,
        text=True,
        capture_output=True,
        check=False
    )
    return process.stdout

def test_clean_corpus_preserved():
    clean_dir = Path('/app/corpus/clean')
    assert clean_dir.exists(), "Clean corpus directory missing."

    modified_files = []
    for csv_file in clean_dir.glob('*.csv'):
        with open(csv_file, 'r') as f:
            original_content = f.read()

        output = run_filter(original_content)

        # Parse output and original to compare rows
        orig_rows = [row for row in csv.reader(original_content.strip().splitlines()) if row]
        out_rows = [row for row in csv.reader(output.strip().splitlines()) if row]

        if orig_rows != out_rows:
            modified_files.append(csv_file.name)

    assert not modified_files, f"{len(modified_files)} clean corpus files were incorrectly modified: {', '.join(modified_files)}"

def test_evil_corpus_rejected():
    evil_dir = Path('/app/corpus/evil')
    assert evil_dir.exists(), "Evil corpus directory missing."

    bypassed_files = []
    for csv_file in evil_dir.glob('*.csv'):
        with open(csv_file, 'r') as f:
            original_content = f.read()

        output = run_filter(original_content)

        # The evil1.csv contains 1 valid row (plus header) and several invalid rows.
        # We need to ensure that only valid rows remain.
        # Let's write a python validator to determine the expected valid rows.
        orig_rows = list(csv.reader(original_content.strip().splitlines()))
        if not orig_rows:
            continue

        header = orig_rows[0]
        expected_rows = [header]
        for row in orig_rows[1:]:
            if len(row) != 5:
                continue
            try:
                ts = int(row[0])
                lat = float(row[1])
                lon = float(row[2])
                alt = float(row[3])
                status = row[4]

                if ts < 0: continue
                if not (-90.0 <= lat <= 90.0): continue
                if not (-180.0 <= lon <= 180.0): continue
                if alt < 0.0: continue
                if status not in ("OK", "WARN", "ERR"): continue

                expected_rows.append(row)
            except ValueError:
                continue

        out_rows = list(csv.reader(output.strip().splitlines()))

        if expected_rows != out_rows:
            bypassed_files.append(csv_file.name)

    assert not bypassed_files, f"{len(bypassed_files)} evil corpus files bypassed validation: {', '.join(bypassed_files)}"

def test_pipeline_outputs_exist():
    assert os.path.isfile('/home/user/clean_telemetry.csv'), "/home/user/clean_telemetry.csv is missing."
    assert os.path.isfile('/home/user/video_features.csv'), "/home/user/video_features.csv is missing."
    assert os.path.isfile('/home/user/merged_output.csv'), "/home/user/merged_output.csv is missing."

def test_merged_output_format():
    merged_path = '/home/user/merged_output.csv'
    with open(merged_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "merged_output.csv is empty."
    header = rows[0]
    expected_header = ['timestamp_sec', 'latitude', 'longitude', 'altitude', 'status', 'brightness']
    assert header == expected_header, f"merged_output.csv header is incorrect. Expected {expected_header}, got {header}"

    if len(rows) > 1:
        assert len(rows[1]) == 6, "merged_output.csv data rows do not have 6 columns."