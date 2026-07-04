# test_final_state.py

import os
import glob
import pytest

def get_expected_events():
    raw_logs_dir = "/home/user/raw_logs"
    csv_files = glob.glob(os.path.join(raw_logs_dir, "*.csv"))

    all_filtered_rows = []

    for file_path in csv_files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Parse and interpolate
        parsed_rows = []
        for i, line in enumerate(lines):
            parts = line.split(",", 3)
            if len(parts) != 4:
                continue
            ts, severity, region, message = parts

            if ts == "MISSING":
                # Find previous and next valid timestamps
                prev_ts = int(lines[i-1].split(",", 1)[0])
                next_ts = int(lines[i+1].split(",", 1)[0])
                ts = str((prev_ts + next_ts) // 2)

            parsed_rows.append((int(ts), severity, region, message))

        # Filter
        for ts, severity, region, message in parsed_rows:
            if severity == "CRITICAL" or "🛑" in message or "故障" in message:
                all_filtered_rows.append((ts, severity, region, message))

    # Sort by timestamp
    all_filtered_rows.sort(key=lambda x: x[0])

    # Format as CSV
    expected_lines = [f"{ts},{sev},{reg},{msg}" for ts, sev, reg, msg in all_filtered_rows]
    return expected_lines

def test_script_exists_and_executable():
    script_path = "/home/user/process_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_critical_events_output():
    output_path = "/home/user/critical_events.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    expected_lines = get_expected_events()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}:\nExpected: {expected}\nActual:   {actual}"