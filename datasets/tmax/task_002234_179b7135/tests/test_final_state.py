# test_final_state.py

import os
import csv
import math

def test_sensor_report_content():
    csv_path = "/home/user/measurements.csv"
    report_path = "/home/user/sensor_report.txt"

    assert os.path.exists(csv_path), f"Input file {csv_path} is missing."
    assert os.path.exists(report_path), f"Output file {report_path} was not generated."

    # Derive expected state from the input CSV
    sensor_data = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
        except StopIteration:
            pass

        for row in reader:
            if len(row) != 3:
                continue
            _, sensor, val_str = row

            # Filter missing values
            if not val_str.strip():
                continue

            try:
                val = float(val_str)
            except ValueError:
                continue

            # Filter outliers
            if val < -10.0 or val > 50.0:
                continue

            if sensor not in sensor_data:
                sensor_data[sensor] = []
            sensor_data[sensor].append(val)

    expected_lines = []
    # Sort alphabetically by sensor name
    for sensor in sorted(sensor_data.keys()):
        vals = sensor_data[sensor]
        if not vals:
            continue

        avg = sum(vals) / len(vals)
        # Round to exactly 2 decimal places
        avg_rounded = round(avg, 2)
        avg_str = f"{avg_rounded:.2f}"

        # Compute asterisks: floor of the average, 0 if negative
        num_asterisks = math.floor(avg)
        if num_asterisks < 0:
            num_asterisks = 0

        plot_str = "*" * num_asterisks
        expected_lines.append(f"Sensor: {sensor} | Avg: {avg_str} | Plot: {plot_str}")

    # Read the actual generated report
    with open(report_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in the report, but found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Mismatch on line {i + 1} of {report_path}.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )