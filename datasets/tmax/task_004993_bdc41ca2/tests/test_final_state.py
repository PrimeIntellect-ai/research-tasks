# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_org.py"
JSON_PATH = "/home/user/evelyn_org.json"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

def test_script_execution_output():
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert "390000" in output, f"Expected total salary '390000' in output, got: '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with error: {e.stderr}")

def test_json_output_exists_and_correct():
    assert os.path.isfile(JSON_PATH), f"JSON output missing at {JSON_PATH}"

    with open(JSON_PATH, "r") as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    expected_json = {
      "name": "Evelyn",
      "salary": 100000,
      "reports": [
        {
          "name": "Bob",
          "salary": 80000,
          "reports": [
            {
              "name": "Dave",
              "salary": 50000,
              "reports": []
            },
            {
              "name": "Eve",
              "salary": 55000,
              "reports": []
            }
          ]
        },
        {
          "name": "Charlie",
          "salary": 60000,
          "reports": [
            {
              "name": "Alice",
              "salary": 45000,
              "reports": []
            }
          ]
        }
      ]
    }

    assert actual_json == expected_json, "The generated JSON structure does not match the expected organizational chart."