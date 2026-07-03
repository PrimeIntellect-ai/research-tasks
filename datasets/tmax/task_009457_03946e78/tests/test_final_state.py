# test_final_state.py

import os
import json
import pytest

PIPELINE_DIR = "/home/user/pipeline"
BAD_IPS_PATH = os.path.join(PIPELINE_DIR, "bad_ips.txt")
SUMMARY_PATH = os.path.join(PIPELINE_DIR, "summary.json")

def test_bad_ips_file():
    assert os.path.isfile(BAD_IPS_PATH), f"Expected file {BAD_IPS_PATH} does not exist."
    with open(BAD_IPS_PATH, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 IP in {BAD_IPS_PATH}, but found {len(lines)}."
    assert lines[0] == "10.0.0.55", f"Expected IP '10.0.0.55' in {BAD_IPS_PATH}, but found '{lines[0]}'."

def test_summary_json_file():
    assert os.path.isfile(SUMMARY_PATH), f"Expected file {SUMMARY_PATH} does not exist."
    with open(SUMMARY_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SUMMARY_PATH} does not contain valid JSON.")

    assert "valid_packets" in data, f"Key 'valid_packets' missing from {SUMMARY_PATH}."
    assert data["valid_packets"] == 4, f"Expected 4 valid packets, but found {data['valid_packets']}."