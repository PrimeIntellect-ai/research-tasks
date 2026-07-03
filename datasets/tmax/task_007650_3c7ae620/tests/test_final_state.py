# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/workspace"
GO_FILE = os.path.join(WORKSPACE_DIR, "process_loc.go")
OUTPUT_FILE = os.path.join(WORKSPACE_DIR, "loc_daily_metrics.csv")

EXPECTED_OUTPUT = """date,lang,total_views,total_edits
2023-10-01,de,200,0
2023-10-01,es,0,2
2023-10-01,fr,200,5
2023-10-02,de,0,10
2023-10-02,fr,100,0
2023-10-03,es,300,15
2023-10-03,fr,0,0"""

def test_go_program_exists():
    assert os.path.isfile(GO_FILE), f"Go program {GO_FILE} does not exist."

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist. Did you run the Go program?"

def test_output_file_content():
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()

    # Normalize line endings
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in EXPECTED_OUTPUT.splitlines() if line.strip()]

    assert content_lines == expected_lines, (
        f"Output file {OUTPUT_FILE} content does not match expected output.\n"
        f"Expected:\n{EXPECTED_OUTPUT}\n\nGot:\n{content}"
    )