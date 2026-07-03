# test_final_state.py

import os
import json
import re
import pytest

def test_directories_and_scripts_exist():
    """Test that required directories and scripts exist."""
    assert os.path.isdir("/home/user/processed"), "/home/user/processed directory is missing."
    assert os.path.isdir("/home/user/experiments"), "/home/user/experiments directory is missing."
    assert os.path.isfile("/home/user/run_pipeline.sh"), "/home/user/run_pipeline.sh script is missing."
    assert os.path.isfile("/home/user/processor.cpp"), "/home/user/processor.cpp is missing."

def test_json_experiments():
    """Test the contents of the experiment JSON files."""
    expected_results = {
        5: {"kept_rows": 8},
        10: {"kept_rows": 0},
        15: {"kept_rows": 0}
    }

    for min_tokens, expected in expected_results.items():
        json_path = f"/home/user/experiments/run_{min_tokens}.json"
        assert os.path.isfile(json_path), f"Experiment JSON {json_path} is missing."

        with open(json_path, "r") as f:
            content = f.read()

        # Parse loosely in case of formatting differences, but require valid JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

        assert data.get("min_tokens") == min_tokens, f"Expected min_tokens={min_tokens} in {json_path}."
        assert data.get("total_rows") == 10, f"Expected total_rows=10 in {json_path}."
        assert data.get("kept_rows") == expected["kept_rows"], f"Expected kept_rows={expected['kept_rows']} in {json_path}."

def test_csv_filtered_5():
    """Test the contents of filtered_5.csv."""
    csv_path = "/home/user/processed/filtered_5.csv"
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 9, f"Expected 9 lines (1 header + 8 data rows) in {csv_path}, found {len(lines)}."
    assert lines[0] == "id,token_count,avg_token_length,rating", "Header of filtered_5.csv is incorrect."

    # Check specific rows
    # id 1: 5 tokens, 19 chars -> 3.80
    assert "1,5,3.80,5" in lines, f"Missing or incorrect row for id=1 in {csv_path}."

    # id 3: 8 tokens, 33 chars -> 4.125 -> 4.12 or 4.13
    id3_found = any(re.match(r"^3,8,4\.1[23],5$", line) for line in lines)
    assert id3_found, f"Missing or incorrect row for id=3 in {csv_path}."

    # id 5: 8 tokens, 42 chars -> 5.25
    assert "5,8,5.25,3" in lines, f"Missing or incorrect row for id=5 in {csv_path}."

def test_csv_filtered_10_and_15():
    """Test that filtered_10.csv and filtered_15.csv only contain the header."""
    for min_tokens in [10, 15]:
        csv_path = f"/home/user/processed/filtered_{min_tokens}.csv"
        assert os.path.isfile(csv_path), f"{csv_path} is missing."

        with open(csv_path, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        assert len(lines) == 1, f"Expected only 1 header line in {csv_path}, found {len(lines)}."
        assert lines[0] == "id,token_count,avg_token_length,rating", f"Header of {csv_path} is incorrect."

def test_reproducibility_check():
    """Test that the reproducibility check file exists and is populated."""
    check_path = "/home/user/reproducibility_check.txt"
    assert os.path.isfile(check_path), f"{check_path} is missing."

    with open(check_path, "r") as f:
        content = f.read().strip()

    assert len(content) > 0, f"{check_path} is empty."

    # Should contain 3 lines for the 3 generated files
    lines = content.split('\n')
    assert len(lines) == 3, f"Expected 3 lines in {check_path}, found {len(lines)}."

    # Each line should look like a sha256 sum
    for line in lines:
        assert re.match(r"^[a-f0-9]{64}\s+.*filtered_\d+\.csv$", line), f"Invalid sha256sum line format: {line}"