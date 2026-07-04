# test_final_state.py

import os
import struct
import csv
import pytest

BASE_DIR = "/home/user/uptime_pipeline"
CONFIG_FILE = "/home/user/.sre_monitor_conf"
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")
METRICS_BIN = os.path.join(BASE_DIR, "data", "raw_metrics.bin")
METRICS_CSV = os.path.join(BASE_DIR, "metrics_output.csv")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

def test_config_file_exists_and_correct():
    assert os.path.isfile(CONFIG_FILE), f"The config file {CONFIG_FILE} was not created."
    with open(CONFIG_FILE, "r") as f:
        content = f.read().strip()
    assert content == "STRICT_MODE", f"Expected config file to contain 'STRICT_MODE', but got '{content}'."

def test_metrics_output_correct():
    assert os.path.isfile(METRICS_CSV), f"The output file {METRICS_CSV} was not generated."

    # Derive expected values from the binary file
    assert os.path.isfile(METRICS_BIN), f"The raw metrics file {METRICS_BIN} is missing."
    with open(METRICS_BIN, "rb") as f:
        data = f.read()

    expected_values = []
    for i in range(len(data) // 8):
        chunk = data[i*8:(i+1)*8]
        val = struct.unpack('d', chunk)[0]
        expected_values.append(f"{val:.5f}")

    # Read the generated CSV
    actual_values = []
    with open(METRICS_CSV, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['MetricID', 'Uptime'], "CSV header is incorrect or missing."
        for row in reader:
            if len(row) == 2:
                actual_values.append(row[1])

    assert actual_values == expected_values, (
        f"Metrics output values do not match expected 64-bit double precision values. "
        f"Expected {expected_values}, got {actual_values}."
    )

def test_report_file_correct():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} was not created."

    # Derive the earliest TIMEOUT timestamp from logs
    min_timestamp = None
    for log_file in os.listdir(LOGS_DIR):
        if log_file.endswith(".log"):
            with open(os.path.join(LOGS_DIR, log_file), "r") as f:
                for line in f:
                    if "TIMEOUT" in line:
                        parts = line.split()
                        if parts and parts[0].isdigit():
                            ts = int(parts[0])
                            if min_timestamp is None or ts < min_timestamp:
                                min_timestamp = ts

    assert min_timestamp is not None, "Could not find any TIMEOUT events in logs to derive expected answer."

    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {REPORT_FILE}, but got {len(lines)}."
    assert lines[0] == CONFIG_FILE, f"Line 1 of report.txt should be '{CONFIG_FILE}', got '{lines[0]}'."
    assert lines[1] == str(min_timestamp), f"Line 2 of report.txt should be the earliest TIMEOUT timestamp '{min_timestamp}', got '{lines[1]}'."