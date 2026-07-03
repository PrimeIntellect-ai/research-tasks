# test_final_state.py

import os
import csv
from datetime import datetime
import pytest

def get_expected_data():
    """Reads the actual sensor data and computes the expected daily aggregations."""
    data = {}

    sensor_a_path = "/home/user/data/sensor_a.csv"
    if os.path.exists(sensor_a_path):
        with open(sensor_a_path, encoding="utf-16le") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
                temp_c = float(row["temp_c"])
                data.setdefault(date_str, []).append(temp_c)

    sensor_b_path = "/home/user/data/sensor_b.csv"
    if os.path.exists(sensor_b_path):
        with open(sensor_b_path, encoding="iso-8859-1") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt = datetime.strptime(row["timestamp"], "%m/%d/%Y-%H:%M")
                date_str = dt.strftime("%Y-%m-%d")
                temp_f = float(row["temp_f"])
                temp_c = (temp_f - 32) * 5.0 / 9.0
                data.setdefault(date_str, []).append(temp_c)

    return data

def test_report_file_exists():
    """Test that the report file was generated in the correct location."""
    report_path = "/home/user/output/report.md"
    assert os.path.isfile(report_path), f"Report file is missing at {report_path}"

def test_report_content():
    """Test that the report content accurately reflects the aggregated sensor data."""
    report_path = "/home/user/output/report.md"
    template_path = "/home/user/template.md"

    assert os.path.isfile(report_path), "Cannot check content because report.md is missing."
    assert os.path.isfile(template_path), "Cannot check content because template.md is missing."

    data = get_expected_data()
    assert data, "No data could be read from the sensor files."

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read().strip()

    expected_blocks = []
    for date_str in sorted(data.keys()):
        temps = data[date_str]
        min_c = min(temps)
        max_c = max(temps)
        avg_c = sum(temps) / len(temps)

        block = template.replace("{DATE}", date_str)
        # Standard float string conversion for min/max, 2 decimal places for avg
        block = block.replace("{MIN}", str(min_c))
        block = block.replace("{MAX}", str(max_c))
        block = block.replace("{AVG}", f"{avg_c:.2f}")
        expected_blocks.append(block)

    expected_output = "\n\n".join(expected_blocks)

    with open(report_path, "r", encoding="utf-8") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        "The generated report content does not match the expected output. "
        "Check your date parsing, temperature conversion, aggregations, and formatting."
    )