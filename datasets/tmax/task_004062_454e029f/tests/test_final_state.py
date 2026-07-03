# test_final_state.py
import os
import pytest
from collections import defaultdict

def test_process_script_exists_and_executable():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_processed_hourly_exists():
    output_path = "/home/user/processed_hourly.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} was not generated."

def test_processed_hourly_content():
    raw_path = "/home/user/raw_sensors.csv"
    output_path = "/home/user/processed_hourly.csv"

    assert os.path.isfile(raw_path), f"Raw file {raw_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(raw_path, "r") as f:
        lines = f.read().splitlines()

    # 1. Filtering: exactly 3 commas
    valid_lines = [line for line in lines if line.count(",") == 3]

    # Exclude header
    if valid_lines and valid_lines[0].startswith("timestamp"):
        valid_lines = valid_lines[1:]

    # 2. Gap-Filling
    records = []
    last_temp = None
    for line in valid_lines:
        parts = line.split(",")
        timestamp = parts[0]
        temp_str = parts[2]

        if temp_str.strip() == "":
            temp = last_temp
        else:
            temp = float(temp_str)
            last_temp = temp

        hour = timestamp[:13] # Extract YYYY-MM-DDTHH
        records.append((hour, temp))

    # 3. Aggregation
    hourly_temps = defaultdict(list)
    for hour, temp in records:
        hourly_temps[hour].append(temp)

    hourly_means = {}
    for hour, temps in hourly_temps.items():
        hourly_means[hour] = sum(temps) / len(temps)

    # 4. Standardization & 5. Formatting
    if not hourly_means:
        expected_lines = []
    else:
        min_mean = min(hourly_means.values())
        max_mean = max(hourly_means.values())

        expected_lines = []
        for hour in sorted(hourly_means.keys()):
            mean = hourly_means[hour]
            if max_mean == min_mean:
                norm = 0.0
            else:
                norm = (mean - min_mean) / (max_mean - min_mean)
            expected_lines.append(f"{hour},{mean:.4f},{norm:.4f}")

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )