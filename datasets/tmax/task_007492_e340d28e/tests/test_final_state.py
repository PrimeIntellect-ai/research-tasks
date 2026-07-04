# test_final_state.py
import os
import json

def test_json_metrics_exported_correctly():
    json_path = '/home/user/session_usage.json'

    assert os.path.exists(json_path), f"The file {json_path} does not exist."
    assert os.path.isfile(json_path), f"The path {json_path} is not a regular file."

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {json_path} does not contain valid JSON."
    except Exception as e:
        assert False, f"Failed to read {json_path}: {e}"

    expected = {
        "sess_alpha": 3072,
        "sess_beta": 500,
        "sess_gamma": 8012
    }

    assert data == expected, f"JSON data does not match expected output. Got {data}, expected {expected}."

def test_bloated_log_symlink():
    log_path = '/home/user/bloated_log.txt'

    # Check if the path exists (or is a broken symlink, but /dev/null should exist)
    assert os.path.lexists(log_path), f"The path {log_path} does not exist at all."
    assert os.path.islink(log_path), f"The path {log_path} is not a symbolic link."

    target = os.readlink(log_path)
    assert target == '/dev/null', f"The symlink {log_path} points to '{target}' instead of '/dev/null'."