# test_final_state.py

import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
RECOVERED_JSON_PATH = os.path.join(PROJECT_DIR, "recovered.json")
PARSE_CONFIG_PATH = os.path.join(PROJECT_DIR, "parse_config.py")
FUZZ_SH_PATH = os.path.join(PROJECT_DIR, "fuzz.sh")
FUZZ_RESULT_PATH = os.path.join(PROJECT_DIR, "fuzz_result.txt")

def test_recovered_json_content():
    assert os.path.isfile(RECOVERED_JSON_PATH), f"Recovered file not found at {RECOVERED_JSON_PATH}"

    expected_content = """[
  {"id": 1, "weight": 10},
  {"id": 2, "weight": "corrupted_value"},
  {"id": 3, "weight": 5}
]
"""
    with open(RECOVERED_JSON_PATH, "r") as f:
        content = f.read()

    # Check exact match as git recovery would yield identical bytes
    assert content.strip() == expected_content.strip(), "Recovered JSON content does not match the original exactly."

def test_parse_config_with_recovered_file():
    assert os.path.isfile(PARSE_CONFIG_PATH), f"Script not found at {PARSE_CONFIG_PATH}"

    result = subprocess.run(
        ["python3", PARSE_CONFIG_PATH, RECOVERED_JSON_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"parse_config.py failed with exit code {result.returncode} on recovered.json"
    assert "Total weight: 15" in result.stdout, "parse_config.py did not output the correct total weight (15)."

def test_parse_config_with_garbage_input(tmp_path):
    garbage_file = tmp_path / "garbage.json"
    garbage_file.write_bytes(os.urandom(50))

    result = subprocess.run(
        ["python3", PARSE_CONFIG_PATH, str(garbage_file)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"parse_config.py did not exit gracefully (code 0) on garbage input. Exit code: {result.returncode}"
    assert "Invalid JSON" in result.stdout, "parse_config.py did not print 'Invalid JSON' when given garbage input."

def test_fuzz_script_properties():
    assert os.path.isfile(FUZZ_SH_PATH), f"Fuzz script not found at {FUZZ_SH_PATH}"
    assert os.access(FUZZ_SH_PATH, os.X_OK), "Fuzz script is not executable."

    with open(FUZZ_SH_PATH, "r") as f:
        content = f.read()

    assert "python3 parse_config.py" in content or "python parse_config.py" in content, "Fuzz script does not appear to invoke parse_config.py"
    assert "for" in content or "while" in content, "Fuzz script does not appear to contain a loop."

def test_fuzz_result_file():
    assert os.path.isfile(FUZZ_RESULT_PATH), f"Fuzz result file not found at {FUZZ_RESULT_PATH}"

    with open(FUZZ_RESULT_PATH, "r") as f:
        content = f.read().strip()

    assert "SUCCESS" in content, "Fuzz result file does not contain 'SUCCESS'."