# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

def test_report_contents():
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert "crashing_packet_index" in data, "Missing 'crashing_packet_index' in report.json"
    assert data["crashing_packet_index"] == 4, f"Expected crashing_packet_index to be 4, got {data['crashing_packet_index']}"

    assert "rip_overwrite_ascii" in data, "Missing 'rip_overwrite_ascii' in report.json"
    assert data["rip_overwrite_ascii"] == "DEADBEEF", f"Expected rip_overwrite_ascii to be 'DEADBEEF', got {data['rip_overwrite_ascii']}"