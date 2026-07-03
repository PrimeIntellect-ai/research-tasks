# test_final_state.py

import os
import subprocess
import pytest

REPORT_PATH = "/home/user/incident_report.txt"
PATCHER_SRC = "/home/user/patcher.rs"
PATCHER_BIN = "/home/user/patcher"
TARGET_BIN = "/home/user/backend_cgi"
PATCHED_BIN = "/home/user/backend_cgi_patched"
EXPECTED_TOKEN = "BDR_w3b_s3cr3t_9921_xyz"
PATCHED_TOKEN = "FIX_w3b_s3cr3t_9921_xyz"

def get_symbol_address(binary_path, symbol_name):
    try:
        result = subprocess.run(
            ["nm", binary_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if symbol_name in line:
                parts = line.split()
                if len(parts) >= 3:
                    return parts[0]
    except subprocess.CalledProcessError:
        pass
    return None

def test_incident_report_content():
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {REPORT_PATH}, found {len(lines)}"

    assert lines[0] == EXPECTED_TOKEN, f"Line 1 of report expected to be '{EXPECTED_TOKEN}', got '{lines[0]}'"

    expected_addr = get_symbol_address(TARGET_BIN, "secret_backdoor_handler")
    assert expected_addr is not None, "Could not find secret_backdoor_handler in the target binary."

    assert lines[1] == expected_addr, f"Line 2 of report expected to be '{expected_addr}', got '{lines[1]}'"

def test_patcher_compiles_and_runs():
    assert os.path.exists(PATCHER_SRC), f"Patcher source not found at {PATCHER_SRC}"

    # Compile the patcher
    compile_result = subprocess.run(
        ["rustc", PATCHER_SRC, "-o", PATCHER_BIN],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert compile_result.returncode == 0, f"Failed to compile {PATCHER_SRC}:\n{compile_result.stderr}"
    assert os.path.exists(PATCHER_BIN), "Compiled patcher binary not found."

    # Run the patcher
    run_result = subprocess.run(
        [PATCHER_BIN, TARGET_BIN],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert run_result.returncode == 0, f"Patcher execution failed:\n{run_result.stderr}"

    assert os.path.exists(PATCHED_BIN), f"Patched binary not found at {PATCHED_BIN}"

def test_patched_binary_content():
    assert os.path.exists(PATCHED_BIN), f"Patched binary not found at {PATCHED_BIN}"

    with open(PATCHED_BIN, "rb") as f:
        content = f.read()

    assert EXPECTED_TOKEN.encode() not in content, f"The original token '{EXPECTED_TOKEN}' is still present in the patched binary."
    assert PATCHED_TOKEN.encode() in content, f"The patched token '{PATCHED_TOKEN}' was not found in the patched binary."