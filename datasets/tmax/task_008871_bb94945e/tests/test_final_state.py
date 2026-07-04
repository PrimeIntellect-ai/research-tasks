# test_final_state.py

import os
import subprocess
import math
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_cron_schedule():
    cron_file = "/home/user/cron_schedule.txt"
    assert os.path.exists(cron_file), f"{cron_file} does not exist."

    # Check if crontab is loaded
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Crontab is not loaded for the user."

    crontab_content = result.stdout
    assert "/home/user/pipeline.sh" in crontab_content, "pipeline.sh is not scheduled in crontab."

    # Check for correct schedule (every 15 minutes)
    valid_schedules = ["*/15", "0,15,30,45"]
    has_valid_schedule = any(sched in crontab_content for sched in valid_schedules)
    assert has_valid_schedule, "Crontab does not contain the correct 15-minute schedule."

def test_pipeline_execution_and_outputs():
    # Run the pipeline to generate outputs
    script_path = "/home/user/pipeline.sh"
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh execution failed:\n{result.stderr}"

    # Verify temp_cleaned.csv
    cleaned_path = "/home/user/temp_cleaned.csv"
    assert os.path.exists(cleaned_path), f"{cleaned_path} was not created."

    with open(cleaned_path, "r") as f:
        cleaned_lines = [line.strip() for line in f if line.strip()]

    expected_cleaned = [
        "1672531200,S1,temp,20.0",
        "1672531200,S3,temp,10.0",
        "1672531210,S1,temp,21.0",
        "1672531210,S3,temp,10.0",
        "1672531220,S1,temp,22.0",
        "1672531220,S3,temp,10.0",
        "1672531230,S1,temp,20.5",
        "1672531230,S3,temp,10.0",
        "1672531240,S1,temp,19.5",
        "1672531240,S3,temp,10.0",
        "1672531250,S1,temp,20.0",
        "1672531260,S1,temp,21.0",
        "1672531270,S1,temp,22.0",
        "1672531280,S1,temp,23.0"
    ]

    # Sorting expected just in case, though it should be chronological
    expected_cleaned.sort(key=lambda x: int(x.split(',')[0]))

    assert cleaned_lines == expected_cleaned, f"Contents of {cleaned_path} do not match expected cleaned data."

    # Verify stats_output.csv
    stats_path = "/home/user/stats_output.csv"
    assert os.path.exists(stats_path), f"{stats_path} was not created."

    with open(stats_path, "r") as f:
        stats_lines = [line.strip() for line in f if line.strip()]

    expected_stats = [
        "1672531240,S1,20.60,0.86",
        "1672531240,S3,10.00,0.00",
        "1672531250,S1,20.60,0.86",
        "1672531260,S1,20.60,0.86",
        "1672531270,S1,20.60,0.86",
        "1672531280,S1,21.10,1.28"
    ]

    # Check if all expected lines are present, order might vary slightly depending on implementation
    for expected in expected_stats:
        assert expected in stats_lines, f"Expected output row '{expected}' not found in {stats_path}"

    assert len(stats_lines) == len(expected_stats), f"Expected exactly {len(expected_stats)} rows in {stats_path}, but found {len(stats_lines)}."