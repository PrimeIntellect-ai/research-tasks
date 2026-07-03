# test_final_state.py

import os
import json
import pytest

BASE_DIR = "/home/user/ticket_8821"
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "summary.json")
RUN_SH_FILE = os.path.join(BASE_DIR, "run.sh")
DATA_FILE = os.path.join(BASE_DIR, "data", "org.json")

def test_summary_json_exists():
    assert os.path.isfile(OUTPUT_FILE), (
        f"The output file {OUTPUT_FILE} was not found. "
        "Ensure the script runs successfully and generates the output."
    )

def test_summary_json_content():
    assert os.path.isfile(OUTPUT_FILE), "Cannot check content, output file is missing."

    with open(OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {OUTPUT_FILE} does not contain valid JSON.")

    expected_counts = {
        "Engineering": 4,
        "Sales": 2,
        "Marketing": 2
    }

    for dept, expected_count in expected_counts.items():
        assert dept in data, f"Department '{dept}' is missing from the output."
        assert data[dept] == expected_count, (
            f"Incorrect count for '{dept}'. Expected {expected_count}, got {data[dept]}. "
            "Ensure cycles are handled, corrupted records are skipped, and race conditions are fixed."
        )

    for dept in data:
        assert dept in expected_counts, f"Unexpected department '{dept}' found in the output."

def test_run_sh_fixed():
    assert os.path.isfile(RUN_SH_FILE), f"The file {RUN_SH_FILE} is missing."
    with open(RUN_SH_FILE, 'r') as f:
        content = f.read()
        assert "/tmp/wrong_data_path" not in content, (
            "The run.sh script still contains the incorrect DATA_DIR path."
        )