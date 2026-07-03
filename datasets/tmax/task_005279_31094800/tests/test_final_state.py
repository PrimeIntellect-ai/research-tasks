# test_final_state.py
import os
import pytest

def get_valid_rows(raw_path):
    valid_rows = []
    with open(raw_path, 'r') as f:
        for line in f:
            if line.count(',') == 4:
                parts = line.strip().split(',')
                try:
                    ts = int(parts[0])
                    temp = float(parts[2])
                    hum = float(parts[3])
                    valid_rows.append((ts, temp, hum))
                except ValueError:
                    pass
    return valid_rows

def get_expected_resampled(valid_rows):
    if not valid_rows:
        return []
    first_ts = valid_rows[0][0]
    last_ts = valid_rows[-1][0]
    resampled = []

    for target_ts in range(first_ts, last_ts + 1, 60):
        latest = None
        for row in valid_rows:
            if row[0] <= target_ts:
                latest = row
            else:
                break
        if latest:
            resampled.append((target_ts, latest[1], latest[2]))
    return resampled

def get_expected_stratified(resampled_rows):
    cold, mod, hot = [], [], []
    for row in resampled_rows:
        temp = row[1]
        if temp < 20.0 and len(cold) < 3:
            cold.append(row)
        elif 20.0 <= temp < 30.0 and len(mod) < 3:
            mod.append(row)
        elif temp >= 30.0 and len(hot) < 3:
            hot.append(row)
    return cold + mod + hot

def format_rows(rows):
    return [f"{ts},{temp:.1f},{hum:.1f}" for ts, temp, hum in rows]

def test_files_exist():
    """Test that all required files and scripts exist."""
    expected_files = [
        "/home/user/clean_resample.c",
        "/home/user/clean_resample",
        "/home/user/stratify.sh",
        "/home/user/resampled.csv",
        "/home/user/stratified.csv"
    ]
    for fpath in expected_files:
        assert os.path.exists(fpath), f"Required file missing: {fpath}"
        assert os.path.isfile(fpath), f"Expected a file but found something else: {fpath}"

    # Check executables
    assert os.access("/home/user/clean_resample", os.X_OK), "/home/user/clean_resample is not executable."
    assert os.access("/home/user/stratify.sh", os.X_OK), "/home/user/stratify.sh is not executable."

def test_resampled_csv():
    """Test that resampled.csv contains the correctly processed and gap-filled data."""
    raw_path = "/home/user/raw_data.csv"
    resampled_path = "/home/user/resampled.csv"

    assert os.path.exists(raw_path), f"Missing {raw_path} to compute expected results."

    valid_rows = get_valid_rows(raw_path)
    expected_rows = get_expected_resampled(valid_rows)
    expected_lines = format_rows(expected_rows)

    with open(resampled_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"resampled.csv content is incorrect.\n"
        f"Expected {len(expected_lines)} lines, got {len(actual_lines)} lines.\n"
        f"Expected first line: {expected_lines[0] if expected_lines else 'None'}\n"
        f"Actual first line: {actual_lines[0] if actual_lines else 'None'}"
    )

def test_stratified_csv():
    """Test that stratified.csv contains exactly 3 records per temperature stratum."""
    raw_path = "/home/user/raw_data.csv"
    stratified_path = "/home/user/stratified.csv"

    valid_rows = get_valid_rows(raw_path)
    resampled_rows = get_expected_resampled(valid_rows)
    expected_rows = get_expected_stratified(resampled_rows)
    expected_lines = format_rows(expected_rows)

    with open(stratified_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"stratified.csv content is incorrect.\n"
        f"Expected exactly 9 lines (3 cold, 3 moderate, 3 hot), got {len(actual_lines)} lines.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )