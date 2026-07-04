# test_final_state.py

import os
import json

def test_success_txt_exists():
    path = "/home/user/ci_task/success.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. Did the PBT script run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "PBT_PASSED", f"Expected {path} to contain 'PBT_PASSED', but got '{content}'."

def test_ws_sanitizer_built():
    path = "/home/user/ci_task/ws_sanitizer"
    assert os.path.isfile(path), f"The executable {path} does not exist. Did you fix the Makefile and run make?"
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_sanitized_json_exists_and_valid():
    path = "/home/user/ci_task/sanitized.json"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you pipe the output to sanitized.json?"

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {path} does not contain valid JSON."

    assert isinstance(data, list), f"Expected JSON array in {path}."
    for item in data:
        assert "input" in item, f"Missing 'input' key in {path}."
        assert "<" not in item["input"], "Unsanitized '<' found in sanitized.json!"
        assert ">" not in item["input"], "Unsanitized '>' found in sanitized.json!"
        assert "alert" not in item["input"], "Unsanitized 'alert' found in sanitized.json!"