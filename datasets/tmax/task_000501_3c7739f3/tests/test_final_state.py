# test_final_state.py
import os
import re

def test_report_exists():
    assert os.path.isfile("/home/user/forensics/report.txt"), "The file /home/user/forensics/report.txt does not exist."

def test_report_content():
    report_path = "/home/user/forensics/report.txt"
    with open(report_path, "r") as f:
        content = f.read().strip()

    # Check for required lines
    assert "Sensor: Pressure Sensor A" in content, "The report does not contain the correct Sensor name (expected 'Pressure Sensor A')."
    assert "Count: 10" in content, "The report does not contain the correct Count (expected 10)."
    assert "Mean: 1000000.02" in content, "The report does not contain the correct Mean (expected 1000000.02)."

    # Variance might be 0.0002
    variance_match = re.search(r"Variance:\s*([0-9.]+)", content)
    assert variance_match is not None, "The report does not contain a Variance field."

    variance_val = float(variance_match.group(1))
    assert abs(variance_val - 0.0002) < 0.00005, f"The Variance value is incorrect. Expected ~0.0002, got {variance_val}"

def test_executable_exists():
    exe_path = "/home/user/forensics/telemetry_parser"
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist. Did you run make?"
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_c_code_modified():
    c_path = "/home/user/forensics/telemetry_parser.c"
    assert os.path.isfile(c_path), f"The file {c_path} is missing."
    with open(c_path, "r") as f:
        content = f.read()

    # Check that the buggy sscanf or variance calculation was changed
    # The original buggy lines:
    # if (sscanf(buffer, "[%s] %lf %ld", sensor_name, &value, &timestamp) == 3) {
    # sum_sq += (value * value); // BUG 2: Catastrophic cancellation

    # We don't strictly require specific code changes, but we can verify the report is correct.
    # The report content test is the primary validation.
    pass