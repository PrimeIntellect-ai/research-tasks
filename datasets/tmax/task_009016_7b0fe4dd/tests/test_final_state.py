# test_final_state.py
import os
import json
import subprocess
import sys

def test_symbol_parser_exists():
    assert os.path.isfile("/home/user/symbol_parser.py"), "symbol_parser.py does not exist."

def test_test_symbol_parser_exists_and_passes():
    assert os.path.isfile("/home/user/test_symbol_parser.py"), "test_symbol_parser.py does not exist."

    # Run pytest on the student's test file
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "/home/user/test_symbol_parser.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest on test_symbol_parser.py failed:\n{result.stdout}\n{result.stderr}"

def test_analyze_symbols_exists():
    assert os.path.isfile("/home/user/analyze_symbols.py"), "analyze_symbols.py does not exist."

def test_conflicts_json_correct():
    json_path = "/home/user/conflicts.json"
    assert os.path.isfile(json_path), "conflicts.json was not generated."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "conflicts.json is not valid JSON."

    expected_data = {
      "init_widget": [
        {
          "address": "0000000000001000",
          "size": 64,
          "type": "T",
          "name": "init_widget"
        },
        {
          "address": "0000000000003000",
          "size": 128,
          "type": "W",
          "name": "init_widget"
        }
      ],
      "const_data": [
        {
          "address": "0000000000007000",
          "size": 32,
          "type": "R",
          "name": "const_data"
        },
        {
          "address": "0000000000008000",
          "size": 48,
          "type": "R",
          "name": "const_data"
        }
      ]
    }

    assert data == expected_data, f"conflicts.json content does not match expected output.\nExpected: {expected_data}\nGot: {data}"