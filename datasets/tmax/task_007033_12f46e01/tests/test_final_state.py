# test_final_state.py

import os
import csv
import subprocess
import re

def test_scripts_exist():
    """Verify that all required Python scripts exist."""
    scripts = [
        "/home/user/reshape.py",
        "/home/user/rolling.py",
        "/home/user/pipeline.py"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Required script {script} is missing."

def test_long_configs_output():
    """Verify the output of the reshape phase."""
    file_path = "/home/user/long_configs.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r', newline='') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 1, f"File {file_path} is empty or has no data."
    header = reader[0]
    expected_header = ["date", "app", "metric", "value"]
    assert header == expected_header, f"Incorrect header in {file_path}. Expected {expected_header}, got {header}."

    # Check a specific row to ensure reshaping and sorting
    # First row after header should be 2023-10-01, app1, threads, 16
    assert reader[1] == ["2023-10-01", "app1", "threads", "16"], f"First data row is incorrect: {reader[1]}"

    # Total rows should be 1 header + 5 dates * 4 metrics = 21
    assert len(reader) == 21, f"Expected 21 rows in {file_path}, got {len(reader)}."

def test_rolling_stats_output():
    """Verify the output of the rolling statistics phase."""
    file_path = "/home/user/rolling_stats.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r', newline='') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 1, f"File {file_path} is empty or has no data."
    header = reader[0]
    expected_header = ["date", "app", "metric", "value", "rolling_mean"]
    assert header == expected_header, f"Incorrect header in {file_path}. Expected {expected_header}, got {header}."

    # Parse data into a dictionary for easy checking
    data = {}
    for row in reader[1:]:
        date, app, metric, value, rolling_mean = row
        key = (date, app, metric)
        data[key] = float(rolling_mean)

    # Check some specific rolling means
    # app1 threads on 2023-10-04: (16+16+32)/3 = 21.33
    key1 = ("2023-10-04", "app1", "threads")
    assert key1 in data, f"Missing data for {key1}"
    assert round(data[key1], 2) == 21.33, f"Expected rolling mean 21.33 for {key1}, got {data[key1]}"

    # app2 workers on 2023-10-03: (2+4+4)/3 = 3.33
    key2 = ("2023-10-03", "app2", "workers")
    assert key2 in data, f"Missing data for {key2}"
    assert round(data[key2], 2) == 3.33, f"Expected rolling mean 3.33 for {key2}, got {data[key2]}"

def test_cron_job_configured():
    """Verify that the cron job is configured correctly for the user."""
    try:
        # Run crontab -l for the current user
        result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        crontab_output = result.stdout
    except Exception as e:
        assert False, f"Failed to check crontab: {e}"

    # Check if there is a cron job running at minute 0 executing pipeline.py
    # Pattern: 0 * * * * ... pipeline.py
    pattern = re.compile(r'^0\s+\*\s+\*\s+\*\s+\*.*pipeline\.py', re.MULTILINE)
    assert pattern.search(crontab_output), "Cron job for pipeline.py at minute 0 is not configured properly."