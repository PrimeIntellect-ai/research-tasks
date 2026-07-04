# test_final_state.py
import os
import csv
from datetime import datetime

RAW_CSV = "/home/user/raw_sensors.csv"
CLEAN_CSV = "/home/user/clean_sensors.csv"
LOG_FILE = "/home/user/cleaning_pipeline.log"
REPORT_FILE = "/home/user/report.md"
TEMPLATE_FILE = "/home/user/report_template.txt"

def process_data():
    if not os.path.exists(RAW_CSV):
        return [], [], 0, 0, 0, 0.0

    valid_rows = []
    rejected_logs = []

    with open(RAW_CSV, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            # Check TIME_PARSE_ERROR
            t_str = row["recorded_at"]
            parsed_time = None
            try:
                parsed_time = datetime.strptime(t_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                try:
                    parsed_time = datetime.strptime(t_str, "%m/%d/%Y %H:%M").strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    pass

            if not parsed_time:
                rejected_logs.append(f"[REJECTED] Row {i}: TIME_PARSE_ERROR")
                continue

            # Check PARSE_ERROR
            try:
                val = float(row["value"])
            except ValueError:
                rejected_logs.append(f"[REJECTED] Row {i}: PARSE_ERROR")
                continue

            # Convert to Celsius
            unit = row["unit"].strip().upper()
            if unit == "F":
                val_c = (val - 32) * 5 / 9
            else:
                val_c = val

            val_c_rounded = round(val_c, 2)

            # Check OUT_OF_BOUNDS
            if val_c_rounded < -50.00 or val_c_rounded > 50.00:
                rejected_logs.append(f"[REJECTED] Row {i}: OUT_OF_BOUNDS")
                continue

            valid_rows.append({
                "sensor_id": row["sensor_id"],
                "recorded_at": parsed_time,
                "value_celsius": f"{val_c_rounded:.2f}"
            })

    total_processed = i
    total_valid = len(valid_rows)
    total_rejected = len(rejected_logs)
    avg_temp = sum(float(r["value_celsius"]) for r in valid_rows) / total_valid if total_valid > 0 else 0.0

    return valid_rows, rejected_logs, total_processed, total_valid, total_rejected, avg_temp

def test_clean_sensors_csv():
    assert os.path.exists(CLEAN_CSV), f"Missing output file: {CLEAN_CSV}"

    expected_valid, _, _, _, _, _ = process_data()

    with open(CLEAN_CSV, "r") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == len(expected_valid), f"Expected {len(expected_valid)} valid rows in clean CSV, got {len(reader)}"

    for i, (actual, expected) in enumerate(zip(reader, expected_valid)):
        assert actual["sensor_id"] == expected["sensor_id"], f"Row {i+1}: expected sensor_id {expected['sensor_id']}, got {actual['sensor_id']}"
        assert actual["recorded_at"] == expected["recorded_at"], f"Row {i+1}: expected recorded_at {expected['recorded_at']}, got {actual['recorded_at']}"

        actual_val = float(actual["value_celsius"])
        expected_val = float(expected["value_celsius"])
        assert abs(actual_val - expected_val) < 0.01, f"Row {i+1}: expected value_celsius {expected_val}, got {actual_val}"

def test_cleaning_pipeline_log():
    assert os.path.exists(LOG_FILE), f"Missing output file: {LOG_FILE}"

    _, expected_logs, _, _, _, _ = process_data()

    with open(LOG_FILE, "r") as f:
        actual_logs = [line.strip() for line in f if line.strip()]

    assert len(actual_logs) == len(expected_logs), f"Expected {len(expected_logs)} logs, got {len(actual_logs)}"

    for i, (actual, expected) in enumerate(zip(actual_logs, expected_logs)):
        assert actual == expected, f"Log line {i+1} mismatch. Expected '{expected}', got '{actual}'"

def test_report_md():
    assert os.path.exists(REPORT_FILE), f"Missing output file: {REPORT_FILE}"
    assert os.path.exists(TEMPLATE_FILE), f"Missing template file: {TEMPLATE_FILE}"

    _, _, total_processed, total_valid, total_rejected, avg_temp = process_data()

    with open(TEMPLATE_FILE, "r") as f:
        template = f.read()

    expected_report = template.replace("{{TOTAL_PROCESSED}}", str(total_processed)) \
                              .replace("{{TOTAL_VALID}}", str(total_valid)) \
                              .replace("{{TOTAL_REJECTED}}", str(total_rejected)) \
                              .replace("{{AVG_TEMP_C}}", f"{avg_temp:.2f}")

    with open(REPORT_FILE, "r") as f:
        actual_report = f.read()

    assert actual_report.strip() == expected_report.strip(), f"Report content mismatch. Expected:\n{expected_report.strip()}\n\nGot:\n{actual_report.strip()}"