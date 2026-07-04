# test_final_state.py
import os
import subprocess
import pytest

def test_leaked_payload_extracted():
    payload_file = "/home/user/leaked_payload.txt"
    assert os.path.exists(payload_file), f"Fail: {payload_file} not found"

    with open(payload_file, "r") as f:
        content = f.read().strip()

    expected_payload = "[SESSION_4815] {{DATA_FRAG_992_UNMATCHED"
    assert content == expected_payload, f"Fail: Incorrect payload extracted. Expected '{expected_payload}', Got: '{content}'"

def test_log_processor_fixed():
    script_path = "/home/user/log_processor.sh"
    assert os.path.exists(script_path), f"Fail: {script_path} not found"

    payload = "[SESSION_4815] {{DATA_FRAG_992_UNMATCHED"

    try:
        result = subprocess.run(
            ["bash", script_path, payload],
            capture_output=True,
            text=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Fail: log_processor.sh still hangs (infinite recursion not fixed)")

    assert result.returncode == 1, f"Fail: Expected exit code 1 for malformed message, got {result.returncode}"
    assert "Malformed message" in result.stdout, "Fail: Script did not echo 'Malformed message' as requested."

def test_processor_patch_exists_and_valid():
    patch_file = "/home/user/processor.patch"
    assert os.path.exists(patch_file), f"Fail: {patch_file} does not exist"
    assert os.path.getsize(patch_file) > 0, f"Fail: {patch_file} is empty"

    with open(patch_file, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, f"Fail: {patch_file} does not look like a unified diff"