# test_final_state.py
import os
import re
import subprocess
import pytest

def get_expected_token():
    dump_path = "/home/user/forensics/memory.dmp"
    if not os.path.exists(dump_path):
        return None
    with open(dump_path, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")
    match = re.search(r"SESSION_TOKEN:([a-f0-9]{32})", content)
    if match:
        return match.group(1)
    return None

def test_token_extracted_correctly():
    token_file = "/home/user/solution/token.txt"
    assert os.path.isfile(token_file), f"Token file missing at {token_file}"

    with open(token_file, "r") as f:
        actual_token = f.read().strip()

    expected_token = get_expected_token()
    assert expected_token is not None, "Could not find expected token in memory dump."

    assert actual_token == expected_token, f"Token in {token_file} is incorrect. Expected {expected_token}, got {actual_token}"

def test_cargo_test_passes():
    app_dir = "/home/user/legacy_app"
    assert os.path.isdir(app_dir), f"Legacy app directory missing at {app_dir}"

    # Run cargo test repeatedly to ensure intermittent failure is fixed
    for i in range(3):
        result = subprocess.run(
            ["cargo", "test"],
            cwd=app_dir,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"`cargo test` failed on run {i+1}. Output:\n{result.stdout}\n{result.stderr}"

def test_lib_rs_deterministic_logic():
    lib_rs_path = "/home/user/legacy_app/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"lib.rs missing at {lib_rs_path}"

    # Just a sanity check that the file is not empty and still contains the function
    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "pub fn get_priority_worker" in content, "get_priority_worker function missing in lib.rs"