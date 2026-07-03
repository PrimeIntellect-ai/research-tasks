# test_final_state.py

import os
import math
import csv
import stat

def test_script_exists_and_executable():
    """Check that the script exists and is executable."""
    script_path = "/home/user/clean_data.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_cleaned_csv_exists():
    """Check that the output file exists."""
    out_path = "/home/user/cleaned_sensors.csv"
    assert os.path.exists(out_path), f"Output file {out_path} does not exist."
    assert os.path.isfile(out_path), f"Path {out_path} is not a file."

def test_cleaned_csv_content():
    """Verify the content of the cleaned dataset according to the task rules."""
    raw_path = "/home/user/raw_sensors.csv"
    out_path = "/home/user/cleaned_sensors.csv"

    # Read raw data and compute magnitudes
    raw_rows = []
    with open(raw_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row:
                continue
            id_, x, y, z, ts = row
            mag = math.sqrt(float(x)**2 + float(y)**2 + float(z)**2)
            raw_rows.append((row, mag))

    # Systematic sample (every 7th data row)
    sample_mags = [mag for i, (row, mag) in enumerate(raw_rows, start=1) if i % 7 == 0]

    # Calculate mean and std
    n = len(sample_mags)
    assert n > 0, "No samples found, raw data might be empty or too short."
    mean = sum(sample_mags) / n
    variance = sum((m - mean)**2 for m in sample_mags) / n
    std = math.sqrt(variance)

    lower_bound = mean - 1.5 * std
    upper_bound = mean + 1.5 * std

    expected_kept = []
    for row, mag in raw_rows:
        if lower_bound < mag < upper_bound:
            expected_kept.append(row + [f"{mag:.4f}"])

    # Read output data
    with open(out_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "Output file must contain at least a header and a stats line."

    # Check header
    out_header = lines[0]
    assert out_header == "id,x,y,z,timestamp,magnitude", f"Incorrect header: {out_header}"

    # Check stats line
    stats_line = lines[-1]
    expected_stats = f"# STATS: mean={mean:.4f}, std={std:.4f}"
    assert stats_line == expected_stats, f"Incorrect stats line. Expected '{expected_stats}', got '{stats_line}'"

    # Check data rows
    data_lines = lines[1:-1]
    assert len(data_lines) == len(expected_kept), f"Expected {len(expected_kept)} data rows, but found {len(data_lines)}."

    for i, (actual, expected) in enumerate(zip(data_lines, expected_kept)):
        actual_parts = actual.split(",")
        assert len(actual_parts) == 6, f"Row {i+1} does not have 6 columns: {actual}"

        # Check first 5 columns exactly
        assert actual_parts[:5] == expected[:5], f"Original columns do not match in row {i+1}. Expected {expected[:5]}, got {actual_parts[:5]}"

        # Check magnitude as float to allow minor formatting differences
        actual_mag = float(actual_parts[5])
        expected_mag = float(expected[5])
        assert math.isclose(actual_mag, expected_mag, abs_tol=1e-4), f"Magnitude mismatch in row {i+1}. Expected ~{expected_mag}, got {actual_mag}"