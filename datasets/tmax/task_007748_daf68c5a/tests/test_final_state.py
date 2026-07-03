# test_final_state.py
import os
import csv
import hashlib
from datetime import datetime, timezone

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline.py"), "/home/user/pipeline.py does not exist."

def test_output_file_exists():
    assert os.path.isfile("/home/user/output_data/clean_data.csv"), "/home/user/output_data/clean_data.csv does not exist."

def test_output_csv_content():
    output_file = "/home/user/output_data/clean_data.csv"

    with open(output_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)

    assert header == ["record_hash", "timestamp", "sensor_id", "temperature", "humidity"], "Header is incorrect."

    expected_rows = [
        ["9f4007b8862f90117a228399f57eb318", "2021-10-01T00:00:00Z", "A", "20.0", "40.0"],
        ["eab4463ce8cba2f30af0a2b535d47065", "2021-10-01T00:01:00Z", "A", "21.0", "41.0"],
        ["ceab44f1c9fc601f0165c7865dc601d3", "2021-10-01T00:02:00Z", "A", "22.0", "42.0"],
        ["ff0af19cd91d4e787bb7b60ffbe52bb8", "2021-10-01T00:03:00Z", "A", "23.0", "43.0"],
        ["106bc666a70d8a4f0bbd4a27572624d5", "2021-10-01T00:00:00Z", "B", "15.0", "50.0"],
        ["601ed85deab587e915002ba50bb5a2e9", "2021-10-01T00:01:00Z", "B", "16.0", "51.0"],
        ["795a98297b5e40632bca60d4b9668d2b", "2021-10-01T00:02:00Z", "B", "17.0", "52.0"]
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(rows)}."

    for i, (row, expected) in enumerate(zip(rows, expected_rows)):
        assert row == expected, f"Row {i+1} mismatch. Expected {expected}, got {row}."

def test_output_csv_formatting_and_logic():
    output_file = "/home/user/output_data/clean_data.csv"
    if not os.path.isfile(output_file):
        return

    with open(output_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        # Check formatting of temperature and humidity
        assert "." in row["temperature"] and len(row["temperature"].split(".")[1]) == 1, f"Temperature {row['temperature']} not formatted to 1 decimal place."
        assert "." in row["humidity"] and len(row["humidity"].split(".")[1]) == 1, f"Humidity {row['humidity']} not formatted to 1 decimal place."

        # Check timestamp format
        try:
            dt = datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            assert False, f"Timestamp {row['timestamp']} does not match ISO8601 UTC format YYYY-MM-DDTHH:MM:SSZ."