# test_final_state.py
import os
import csv
from datetime import datetime, timedelta
import pytest

def parse_datetime(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")

def format_hour(dt):
    return dt.strftime("%Y-%m-%dT%H")

def format_day(dt):
    return dt.strftime("%Y-%m-%d")

def compute_expected_report():
    input_file = "/home/user/sensor_data.csv"
    if not os.path.exists(input_file):
        pytest.fail(f"Input file {input_file} is missing.")

    buckets = {}

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = parse_datetime(row["timestamp"])
            hour_key = format_hour(dt)
            temp = float(row["temperature"])
            hum = float(row["humidity"])

            if hour_key not in buckets:
                buckets[hour_key] = {"temp_sum": 0.0, "hum_sum": 0.0, "count": 0}

            buckets[hour_key]["temp_sum"] += temp
            buckets[hour_key]["hum_sum"] += hum
            buckets[hour_key]["count"] += 1

    if not buckets:
        return ""

    # Calculate means
    hourly_data = {}
    for k, v in buckets.items():
        hourly_data[k] = {
            "temp": v["temp_sum"] / v["count"],
            "hum": v["hum_sum"] / v["count"]
        }

    # Get min and max hours
    sorted_hours = sorted(hourly_data.keys())
    min_hour_dt = datetime.strptime(sorted_hours[0], "%Y-%m-%dT%H")
    max_hour_dt = datetime.strptime(sorted_hours[-1], "%Y-%m-%dT%H")

    # Generate full range
    full_range = []
    current_dt = min_hour_dt
    while current_dt <= max_hour_dt:
        full_range.append(format_hour(current_dt))
        current_dt += timedelta(hours=1)

    # Interpolation
    for i, h in enumerate(full_range):
        if h not in hourly_data:
            # Find prev
            prev_idx = i - 1
            while prev_idx >= 0 and full_range[prev_idx] not in hourly_data:
                prev_idx -= 1
            # Find next
            next_idx = i + 1
            while next_idx < len(full_range) and full_range[next_idx] not in hourly_data:
                next_idx += 1

            prev_h = full_range[prev_idx]
            next_h = full_range[next_idx]

            prev_temp, prev_hum = hourly_data[prev_h]["temp"], hourly_data[prev_h]["hum"]
            next_temp, next_hum = hourly_data[next_h]["temp"], hourly_data[next_h]["hum"]

            fraction = (i - prev_idx) / (next_idx - prev_idx)

            hourly_data[h] = {
                "temp": prev_temp + (next_temp - prev_temp) * fraction,
                "hum": prev_hum + (next_hum - prev_hum) * fraction,
                "interpolated": True
            }

    # Calculate stress index and group by day
    daily_max = {}
    for h in full_range:
        day = h[:10]
        temp = hourly_data[h]["temp"]
        hum = hourly_data[h]["hum"]
        stress_index = (temp * 1.5) + (hum * 0.5)

        if day not in daily_max or stress_index > daily_max[day]:
            daily_max[day] = stress_index

    lines = []
    for day in sorted(daily_max.keys()):
        lines.append(f"Date: {day} - Max Stress Index: {daily_max[day]:.2f}")

    return "\n".join(lines)

def test_daily_report_exists_and_correct():
    report_file = "/home/user/daily_report.txt"
    assert os.path.exists(report_file), f"Report file {report_file} does not exist."
    assert os.path.isfile(report_file), f"Path {report_file} is not a file."

    expected_content = compute_expected_report()

    with open(report_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {report_file} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Got:\n{actual_content}"
    )