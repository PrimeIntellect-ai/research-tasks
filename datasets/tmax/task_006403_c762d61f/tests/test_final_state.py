# test_final_state.py

import os
import json

def test_exploit_script_exists():
    exploit_path = "/home/user/exploit.go"
    assert os.path.exists(exploit_path), f"Exploit script not found at {exploit_path}"
    assert os.path.isfile(exploit_path), f"{exploit_path} is not a file"

def test_rotation_result_exists_and_correct():
    result_path = "/home/user/rotation_result.json"
    assert os.path.exists(result_path), f"Output file not found at {result_path}"
    assert os.path.isfile(result_path), f"{result_path} is not a file"

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content, "The rotation result file is empty"

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        assert False, f"The content of {result_path} is not valid JSON"

    assert data.get("status") == "success", "The rotation response status is not 'success'"
    assert data.get("new_key") == "SECRET_KEY_998877_ROTATED", "The rotation response does not contain the expected new key"