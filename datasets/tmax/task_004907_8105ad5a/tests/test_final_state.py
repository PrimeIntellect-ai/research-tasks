# test_final_state.py

import os
import json
import configparser

def test_parser_script_exists():
    """Verify that the parser script was created."""
    script_path = "/home/user/parser.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_json_output_exists():
    """Verify that the JSON output file was created."""
    json_path = "/home/user/safe_extraction_plan.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

def test_json_output_content():
    """Verify that the JSON output contains the correct data derived from the manifests."""
    json_path = "/home/user/safe_extraction_plan.json"

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {json_path} does not contain valid JSON."

    # Expected values based on the provided setup
    expected_safe_files = sorted([
        "dir/café.txt",
        "dir/file2.txt",
        "file1.txt",
        "legit_file.dat"
    ])
    expected_total_bytes = 1024 + 2048 + 4096 + 100
    expected_malicious_skipped = 2

    assert "total_safe_bytes" in data, "Missing 'total_safe_bytes' in JSON output."
    assert data["total_safe_bytes"] == expected_total_bytes, f"Expected total_safe_bytes to be {expected_total_bytes}, got {data['total_safe_bytes']}."

    assert "safe_files" in data, "Missing 'safe_files' in JSON output."
    assert isinstance(data["safe_files"], list), "'safe_files' should be a list."
    assert data["safe_files"] == expected_safe_files, f"Expected safe_files to be {expected_safe_files}, got {data['safe_files']}."

    assert "malicious_files_skipped" in data, "Missing 'malicious_files_skipped' in JSON output."
    assert data["malicious_files_skipped"] == expected_malicious_skipped, f"Expected malicious_files_skipped to be {expected_malicious_skipped}, got {data['malicious_files_skipped']}."