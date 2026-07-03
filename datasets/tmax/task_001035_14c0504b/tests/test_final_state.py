# test_final_state.py
import os
import csv
import math
import subprocess
import pytest
from pathlib import Path

def reference_cleaner(input_lines):
    reader = csv.DictReader(input_lines)
    fieldnames = reader.fieldnames
    output_rows = []
    window = []
    last_timestamp = -float('inf')

    for row in reader:
        try:
            ts = float(row['timestamp'])
            x = float(row['x'])
            y = float(row['y'])
            z = float(row['z'])
        except ValueError:
            continue

        if ts <= last_timestamp:
            continue

        curr_window = window[-4:] + [(x, y, z)]
        cx = sum(p[0] for p in curr_window) / len(curr_window)
        cy = sum(p[1] for p in curr_window) / len(curr_window)
        cz = sum(p[2] for p in curr_window) / len(curr_window)

        dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)

        if dist > 10.0:
            continue

        last_timestamp = ts
        window.append((x, y, z))
        output_rows.append(row)

    return fieldnames, output_rows

def run_student_cleaner(executable, input_path):
    with open(input_path, 'r') as f:
        input_data = f.read()

    result = subprocess.run(
        [executable],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )
    return result.stdout.strip().splitlines()

def test_executable_exists():
    executable = '/home/user/cleaner'
    assert os.path.isfile(executable), f"Executable {executable} not found. Did you compile your C++ program?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_clean_corpus():
    executable = '/home/user/cleaner'
    clean_dir = Path('/app/data/clean_corpus')

    if not clean_dir.exists():
        pytest.skip("Clean corpus directory not found.")

    failed_files = []

    for csv_file in clean_dir.glob('*.csv'):
        with open(csv_file, 'r') as f:
            lines = f.read().strip().splitlines()

        expected_fieldnames, expected_rows = reference_cleaner(lines)

        student_output = run_student_cleaner(executable, csv_file)
        if not student_output:
            failed_files.append(csv_file.name)
            continue

        student_reader = csv.DictReader(student_output)
        student_rows = list(student_reader)

        if len(student_rows) != len(expected_rows):
            failed_files.append(csv_file.name)
            continue

    assert not failed_files, f"{len(failed_files)} clean corpus files failed or were modified: {', '.join(failed_files)}"

def test_evil_corpus():
    executable = '/home/user/cleaner'
    evil_dir = Path('/app/data/evil_corpus')

    if not evil_dir.exists():
        pytest.skip("Evil corpus directory not found.")

    failed_files = []

    for csv_file in evil_dir.glob('*.csv'):
        with open(csv_file, 'r') as f:
            lines = f.read().strip().splitlines()

        expected_fieldnames, expected_rows = reference_cleaner(lines)

        student_output = run_student_cleaner(executable, csv_file)
        if not student_output:
            if expected_rows:
                failed_files.append(csv_file.name)
            continue

        student_reader = csv.DictReader(student_output)
        student_rows = list(student_reader)

        if len(student_rows) != len(expected_rows):
            failed_files.append(csv_file.name)
            continue

        # Check if the timestamps match exactly
        expected_ts = [float(r['timestamp']) for r in expected_rows]
        student_ts = [float(r['timestamp']) for r in student_rows]

        if expected_ts != student_ts:
            failed_files.append(csv_file.name)

    assert not failed_files, f"{len(failed_files)} evil corpus files bypassed validation: {', '.join(failed_files)}"