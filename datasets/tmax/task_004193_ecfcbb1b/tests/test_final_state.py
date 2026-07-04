# test_final_state.py
import os
import re
import gzip
import glob
import math
import pytest

RAW_DATA_DIR = "/home/user/raw_data"
CLEAN_DATA_CSV = "/home/user/clean_data/combined.csv"
GZ_LABEL_0 = "/home/user/processed_data/label_0/data.csv.gz"
GZ_LABEL_1 = "/home/user/processed_data/label_1/data.csv.gz"
MEAN_DIFF_TXT = "/home/user/metrics/mean_diff.txt"
CV_FOLDS_DIR = "/home/user/cv_folds"
SCRIPTS_DIR = "/home/user/scripts"

def is_valid_row(line):
    parts = line.strip().split(',')
    if len(parts) != 4:
        return False

    # Column 1: positive integer
    if not re.match(r'^[1-9][0-9]*$', parts[0]):
        return False

    # Column 2: ISO-8601 YYYY-MM-DDTHH:MM:SSZ
    if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$', parts[1]):
        return False

    # Column 3: valid floating-point number
    if not re.match(r'^-?[0-9]+(\.[0-9]+)?$', parts[2]):
        return False

    # Column 4: exactly 0 or 1
    if parts[3] not in ['0', '1']:
        return False

    return True

def test_scripts_exist_and_executable():
    for script_name in ["validate.sh", "kfold.sh"]:
        script_path = os.path.join(SCRIPTS_DIR, script_name)
        assert os.path.isfile(script_path), f"Script {script_path} does not exist."
        assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_combined_csv_valid():
    assert os.path.isfile(CLEAN_DATA_CSV), f"Clean data file {CLEAN_DATA_CSV} does not exist."

    # Compute expected valid rows from raw data
    raw_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
    expected_valid_lines = []
    for raw_file in raw_files:
        with open(raw_file, 'r') as f:
            for line in f:
                if is_valid_row(line):
                    expected_valid_lines.append(line.strip())

    # Read actual combined.csv
    with open(CLEAN_DATA_CSV, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_valid_lines), (
        f"Expected {len(expected_valid_lines)} valid rows, but found {len(actual_lines)} in {CLEAN_DATA_CSV}."
    )

    # Verify all actual rows are valid
    for i, line in enumerate(actual_lines):
        assert is_valid_row(line), f"Row {i+1} in {CLEAN_DATA_CSV} is invalid: {line}"

def test_gzipped_partitions():
    assert os.path.isfile(GZ_LABEL_0), f"Gzip file {GZ_LABEL_0} does not exist."
    assert os.path.isfile(GZ_LABEL_1), f"Gzip file {GZ_LABEL_1} does not exist."

    # Read combined.csv to get expected partitions
    expected_0 = []
    expected_1 = []
    with open(CLEAN_DATA_CSV, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if parts[3] == '0':
                expected_0.append(line)
            elif parts[3] == '1':
                expected_1.append(line)

    # Read gzip files
    try:
        with gzip.open(GZ_LABEL_0, 'rt') as f:
            actual_0 = [line.strip() for line in f if line.strip()]
    except Exception as e:
        pytest.fail(f"Failed to read {GZ_LABEL_0} as a gzip file: {e}")

    try:
        with gzip.open(GZ_LABEL_1, 'rt') as f:
            actual_1 = [line.strip() for line in f if line.strip()]
    except Exception as e:
        pytest.fail(f"Failed to read {GZ_LABEL_1} as a gzip file: {e}")

    assert sorted(actual_0) == sorted(expected_0), f"Contents of {GZ_LABEL_0} do not match the label 0 rows in {CLEAN_DATA_CSV}."
    assert sorted(actual_1) == sorted(expected_1), f"Contents of {GZ_LABEL_1} do not match the label 1 rows in {CLEAN_DATA_CSV}."

def test_mean_diff():
    assert os.path.isfile(MEAN_DIFF_TXT), f"Metrics file {MEAN_DIFF_TXT} does not exist."

    sum0, cnt0 = 0.0, 0
    sum1, cnt1 = 0.0, 0
    with open(CLEAN_DATA_CSV, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            val = float(parts[2])
            if parts[3] == '0':
                sum0 += val
                cnt0 += 1
            elif parts[3] == '1':
                sum1 += val
                cnt1 += 1

    assert cnt0 > 0 and cnt1 > 0, "Not enough data to compute means."
    expected_diff = abs((sum1 / cnt1) - (sum0 / cnt0))
    expected_diff_str = f"{expected_diff:.4f}"

    with open(MEAN_DIFF_TXT, 'r') as f:
        actual_diff_str = f.read().strip()

    assert actual_diff_str == expected_diff_str, (
        f"Expected mean difference {expected_diff_str}, but got {actual_diff_str} in {MEAN_DIFF_TXT}."
    )

def test_cv_folds():
    fold_files = [os.path.join(CV_FOLDS_DIR, f"fold_{i}.csv") for i in range(1, 6)]
    for f in fold_files:
        assert os.path.isfile(f), f"Fold file {f} does not exist."

    fold_lines = []
    for f in fold_files:
        with open(f, 'r') as file:
            fold_lines.extend([line.strip() for line in file if line.strip()])

    with open(CLEAN_DATA_CSV, 'r') as f:
        original_lines = [line.strip() for line in f if line.strip()]

    assert len(fold_lines) == len(original_lines), (
        f"Total lines in folds ({len(fold_lines)}) does not match lines in {CLEAN_DATA_CSV} ({len(original_lines)})."
    )

    assert sorted(fold_lines) == sorted(original_lines), (
        "The combined contents of the fold files do not exactly match the contents of the original clean data."
    )