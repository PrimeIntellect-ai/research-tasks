# test_final_state.py
import os
import csv

def test_process_logs_script_exists():
    script_path = "/home/user/process_logs.py"
    assert os.path.exists(script_path), f"Script file {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_critical_hourly_summary_exists():
    output_path = "/home/user/critical_hourly_summary.csv"
    assert os.path.exists(output_path), f"Output file {output_path} is missing. Did you run your script?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_critical_hourly_summary_content():
    output_path = "/home/user/critical_hourly_summary.csv"

    with open(output_path, "r", newline="") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "The output CSV is empty."

    header = reader[0]
    assert header == ["hour_timestamp", "event_count"], \
        f"Incorrect header. Expected ['hour_timestamp', 'event_count'], got {header}."

    rows = reader[1:]
    assert len(rows) == 2, f"Expected exactly 2 data rows, got {len(rows)}."

    expected_data = [
        ["2023-10-15T14:00:00Z", "2"],
        ["2023-10-16T02:00:00Z", "2"]
    ]

    assert rows == expected_data, \
        f"Output data does not match expected results or is not sorted chronologically. Got {rows}."