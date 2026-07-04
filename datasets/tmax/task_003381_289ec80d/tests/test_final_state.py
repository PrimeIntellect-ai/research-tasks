# test_final_state.py
import os
import csv
import json
import hashlib
import glob
from datetime import datetime, timedelta
import pytest

def test_script_exists():
    assert os.path.exists("/home/user/process_sensors.py"), "The script /home/user/process_sensors.py is missing."
    assert os.path.isfile("/home/user/process_sensors.py"), "/home/user/process_sensors.py is not a file."

def test_output_json_exists():
    assert os.path.exists("/home/user/rolling_averages.json"), "The output file /home/user/rolling_averages.json is missing."
    assert os.path.isfile("/home/user/rolling_averages.json"), "/home/user/rolling_averages.json is not a file."

def test_output_json_content():
    # Read and process data to compute expected result
    files = glob.glob("/home/user/sensor_data/shard_*.csv")
    assert files, "No shard files found in /home/user/sensor_data/"

    records_by_hash = {}

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                event_time = row["event_time"]
                sensor_id = row["sensor_id"]
                temperature = float(row["temperature"])
                ingested_at = int(row["ingested_at"])

                hash_str = f"{event_time}{sensor_id}{temperature:.1f}"
                row_hash = hashlib.md5(hash_str.encode("utf-8")).hexdigest()

                if row_hash not in records_by_hash:
                    records_by_hash[row_hash] = row
                else:
                    if ingested_at > int(records_by_hash[row_hash]["ingested_at"]):
                        records_by_hash[row_hash] = row

    # Group by sensor and date
    daily_data = {}
    for row in records_by_hash.values():
        sensor_id = row["sensor_id"]
        date_str = row["event_time"][:10]
        temp = float(row["temperature"])

        if sensor_id not in daily_data:
            daily_data[sensor_id] = {}
        if date_str not in daily_data[sensor_id]:
            daily_data[sensor_id][date_str] = []

        daily_data[sensor_id][date_str].append(temp)

    # Calculate daily averages
    daily_averages = {}
    for sensor, dates in daily_data.items():
        daily_averages[sensor] = {}
        for date_str, temps in dates.items():
            daily_averages[sensor][date_str] = sum(temps) / len(temps)

    # Calculate 3-day rolling averages
    expected_result = {}
    for sensor, dates in daily_averages.items():
        expected_result[sensor] = {}
        sorted_dates = sorted(dates.keys())

        for date_str in sorted_dates:
            current_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            window_dates = [
                (current_date - timedelta(days=i)).strftime("%Y-%m-%d") 
                for i in range(3)
            ]

            window_temps = [
                daily_averages[sensor][d] 
                for d in window_dates 
                if d in daily_averages[sensor]
            ]

            rolling_avg = sum(window_temps) / len(window_temps)
            expected_result[sensor][date_str] = round(rolling_avg, 2)

    # Read student's output
    with open("/home/user/rolling_averages.json", "r", encoding="utf-8") as f:
        try:
            student_result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/rolling_averages.json is not valid JSON.")

    # Compare
    for sensor, dates in expected_result.items():
        assert sensor in student_result, f"Sensor {sensor} missing from output."
        for date_str, expected_val in dates.items():
            assert date_str in student_result[sensor], f"Date {date_str} for sensor {sensor} missing from output."
            student_val = student_result[sensor][date_str]
            assert abs(student_val - expected_val) < 1e-5, f"Mismatch for {sensor} on {date_str}: expected {expected_val}, got {student_val}."

    for sensor in student_result:
        assert sensor in expected_result, f"Unexpected sensor {sensor} in output."
        for date_str in student_result[sensor]:
            assert date_str in expected_result[sensor], f"Unexpected date {date_str} for sensor {sensor} in output."