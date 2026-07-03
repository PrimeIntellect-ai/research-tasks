# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_assets.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution():
    script_path = "/home/user/process_assets.sh"
    # Run the script to ensure it compiles the C code and processes the manifests without ASAN errors
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute or ASAN error occurred. Stderr: {result.stderr}"

def test_summary_log_contents():
    log_path = "/home/user/summary.log"
    assert os.path.isfile(log_path), f"Summary log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "AUDIO: 640",
        "METADATA: 64",
        "MODEL: 5120",
        "TEXTURE: 3072",
        "TEXTURE_HIGH_RESOLUTION_ASSET_NAME_OVER_SIXTEEN_CHARS: 8192"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {log_path} do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )