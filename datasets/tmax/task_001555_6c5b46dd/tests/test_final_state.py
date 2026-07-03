# test_final_state.py
import os
import csv

def test_cleaned_summary_exists():
    assert os.path.isfile('/home/user/cleaned_summary.csv'), "Output file /home/user/cleaned_summary.csv does not exist."

def test_cleaned_summary_content():
    expected_header = ["user_id", "event_count", "avg_latency", "high_latency_count"]
    expected_rows = [
        ["1", "2", "1000.0", "1"],
        ["2", "1", "1200.0", "1"],
        ["3", "1", "200.0", "0"],
        ["4", "1", "1050.0", "1"]
    ]

    with open('/home/user/cleaned_summary.csv', 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The file /home/user/cleaned_summary.csv is empty."

    header = rows[0]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(data_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_rows, data_rows)):
        # For avg_latency, allow slight floating point formatting differences (e.g., "1000.0" vs "1000.00")
        assert actual[0] == expected[0], f"Row {i+1}: Expected user_id {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1}: Expected event_count {expected[1]}, got {actual[1]}"
        assert float(actual[2]) == float(expected[2]), f"Row {i+1}: Expected avg_latency {expected[2]}, got {actual[2]}"
        assert actual[3] == expected[3], f"Row {i+1}: Expected high_latency_count {expected[3]}, got {actual[3]}"

def test_script_exists():
    assert os.path.isfile('/home/user/clean_data.py'), "The script /home/user/clean_data.py was not found."