# test_final_state.py

import os
import json
import pytest

def test_fast_stat_executable():
    binary_path = "/home/user/legacy_tool/fast-stat"
    assert os.path.isfile(binary_path), f"The compiled binary {binary_path} does not exist. Did you run make?"
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_makefile_fixed():
    makefile_path = "/home/user/legacy_tool/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        lines = f.readlines()

    content = "".join(lines)
    assert "-Wmissing-headers" not in content, "The invalid '-Wmissing-headers' flag is still in the Makefile."

    has_tab_indent = any(line.startswith("\tgcc") for line in lines)
    assert has_tab_indent, "The Makefile does not have a properly tab-indented 'gcc' command for the fast-stat target."

def test_c_file_fixed():
    c_file_path = "/home/user/legacy_tool/fast-stat.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "/var/log/legacy_telemetry.log" not in content, "The hardcoded file path is still present in the C source code."
    assert "DATA_FILE" in content, "The C source code does not seem to read the 'DATA_FILE' environment variable."
    assert "<stdlib.h>" in content, "The C source code is missing the <stdlib.h> include."
    assert "<string.h>" in content, "The C source code is missing the <string.h> include."

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} was not generated."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "records" in data, "The JSON report is missing the 'records' key."
    assert "anomalies" in data, "The JSON report is missing the 'anomalies' key."
    assert "duration" in data, "The JSON report is missing the 'duration' key."

    assert data["records"] == 7, f"Expected 7 records, but got {data['records']}."
    assert data["anomalies"] == 2, f"Expected 2 anomalies, but got {data['anomalies']}."
    assert data["duration"] == 42, f"Expected duration of 42, but got {data['duration']}."