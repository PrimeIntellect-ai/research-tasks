# test_final_state.py
import os
import json
import subprocess
import re
import pytest

def test_resolution_json_exists():
    assert os.path.isfile("/home/user/resolution.json"), "/home/user/resolution.json does not exist."

def test_resolution_json_content():
    # Dynamically find the expected bad commit hash based on the commit message
    repo_dir = "/home/user/sim_repo"
    try:
        output = subprocess.check_output(
            ["git", "log", "--grep=Optimize calculation logic", "--format=%H"],
            cwd=repo_dir,
            text=True
        )
        expected_commit = output.strip().split('\n')[0]
    except Exception as e:
        pytest.fail(f"Could not retrieve expected commit from git history: {e}")

    assert expected_commit, "Failed to locate the expected bad commit in git history."

    # Dynamically extract the expected panic string from the binary dump
    dump_path = "/home/user/logs/dump.bin"
    expected_panic = None
    try:
        with open(dump_path, "rb") as f:
            content = f.read()
        # Look for PANIC_LOG: followed by uppercase letters, numbers, and underscores
        match = re.search(b"PANIC_LOG:[A-Z0-9_]+", content)
        if match:
            expected_panic = match.group(0).decode("ascii")
    except Exception as e:
        pytest.fail(f"Could not read or parse dump.bin: {e}")

    assert expected_panic is not None, "Could not find the expected PANIC_LOG string in dump.bin."

    # Parse the student's resolution.json
    try:
        with open("/home/user/resolution.json", "r") as f:
            resolution = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not parse /home/user/resolution.json as valid JSON: {e}")

    # Validate keys and values
    assert "bad_commit" in resolution, "'bad_commit' key is missing in resolution.json."
    assert "panic_string" in resolution, "'panic_string' key is missing in resolution.json."

    actual_commit = resolution["bad_commit"].strip()
    actual_panic = resolution["panic_string"].strip()

    assert actual_commit == expected_commit, (
        f"The 'bad_commit' value is incorrect.\n"
        f"Expected: {expected_commit}\n"
        f"Found: {actual_commit}\n"
        f"Did you identify the exact commit that introduced the precision loss?"
    )

    assert actual_panic == expected_panic, (
        f"The 'panic_string' value is incorrect.\n"
        f"Expected: {expected_panic}\n"
        f"Found: {actual_panic}\n"
        f"Did you correctly extract the full PANIC_LOG string from dump.bin?"
    )