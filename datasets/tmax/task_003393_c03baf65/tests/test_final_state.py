# test_final_state.py

import os
import json
import subprocess
import pytest

def get_expected_entry_point(filepath):
    """Helper to dynamically extract the entry point address from an ELF file."""
    try:
        result = subprocess.run(['readelf', '-h', filepath], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "Entry point address:" in line:
                return line.split(":", 1)[1].strip()
    except Exception as e:
        pytest.fail(f"Failed to run readelf to determine expected entry point: {e}")
    return None

def test_merged_gcode_exists():
    """Test that the merged GCode file was created."""
    merged_file = "/home/user/merged_print.gcode"
    assert os.path.isfile(merged_file), f"The merged GCode file {merged_file} does not exist."

def test_report_exists():
    """Test that the final JSON report exists."""
    report_file = "/home/user/report.json"
    assert os.path.isfile(report_file), f"The report file {report_file} does not exist."

def test_report_contents():
    """Test that the JSON report contains the correct extracted information."""
    report_file = "/home/user/report.json"

    with open(report_file, 'r', encoding='utf-8') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_file} does not contain valid JSON.")

    expected_firmware_path = "/home/user/firmwares/v2.elf"
    expected_total_extrusion = 12.0

    # 1. Check latest_firmware_path
    assert "latest_firmware_path" in report, "Key 'latest_firmware_path' is missing from report.json."
    assert report["latest_firmware_path"] == expected_firmware_path, \
        f"Expected latest_firmware_path to be '{expected_firmware_path}', but got '{report['latest_firmware_path']}'."

    # 2. Check total_extrusion
    assert "total_extrusion" in report, "Key 'total_extrusion' is missing from report.json."
    assert isinstance(report["total_extrusion"], (int, float)), "Value for 'total_extrusion' must be a number."
    assert abs(report["total_extrusion"] - expected_total_extrusion) < 1e-5, \
        f"Expected total_extrusion to be {expected_total_extrusion}, but got {report['total_extrusion']}."

    # 3. Check firmware_entry_point
    assert "firmware_entry_point" in report, "Key 'firmware_entry_point' is missing from report.json."

    expected_entry_point = get_expected_entry_point(expected_firmware_path)
    assert expected_entry_point is not None, "Could not determine the expected entry point from the ELF file."

    # Allow case-insensitive comparison and optional zero-padding if standard tools format it slightly differently,
    # but the task specified "exactly as formatted by standard tools".
    assert report["firmware_entry_point"].lower() == expected_entry_point.lower(), \
        f"Expected firmware_entry_point to be '{expected_entry_point}', but got '{report['firmware_entry_point']}'."