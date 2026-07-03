# test_final_state.py

import os
import csv
import pytest

REPORT_PATH = "/home/user/report.csv"

def test_report_exists():
    """Check if the report.csv file exists."""
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

def test_report_content():
    """Check if the report contains the correct data and formatting."""
    expected_data = [
        ("2023-10-01", 250.0, "250.00"),
        ("2023-10-02", 200.0, "225.00"),
        ("2023-10-03", 300.0, "250.00"),
        ("2023-10-04", 100.0, "200.00"),
        ("2023-10-05", 50.0, "150.00"),
        ("2023-10-06", 400.0, "183.33"),
        ("2023-10-07", 100.0, "183.33")
    ]

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("The report.csv file is empty.")

        assert header == ["date", "daily_total", "rolling_avg"], \
            f"CSV header is incorrect. Expected ['date', 'daily_total', 'rolling_avg'], got {header}"

        rows = list(reader)
        assert len(rows) == len(expected_data), \
            f"Expected {len(expected_data)} rows of data, but got {len(rows)}."

        for i, (row, expected) in enumerate(zip(rows, expected_data)):
            assert len(row) == 3, f"Row {i+1} does not have exactly 3 columns: {row}"

            date, daily_total_str, rolling_avg_str = row
            exp_date, exp_daily_total, exp_rolling_avg_str = expected

            assert date == exp_date, f"Row {i+1}: Expected date {exp_date}, got {date}"

            try:
                daily_total = float(daily_total_str)
            except ValueError:
                pytest.fail(f"Row {i+1}: Cannot parse daily_total '{daily_total_str}' as a float.")

            assert abs(daily_total - exp_daily_total) < 1e-5, \
                f"Row {i+1}: Expected daily_total {exp_daily_total}, got {daily_total}"

            assert rolling_avg_str == exp_rolling_avg_str, \
                f"Row {i+1}: Expected rolling_avg '{exp_rolling_avg_str}', got '{rolling_avg_str}' (must be exactly 2 decimal places)"