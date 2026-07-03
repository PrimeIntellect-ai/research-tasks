# test_final_state.py

import os
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = '/home/user/api_gateway/Makefile'
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist."

    with open(makefile_path, 'r') as f:
        content = f.read()

    # Check if rate_limit.o is in the linking step
    # The original was: $(CXX) $(CXXFLAGS) main.o checksum.o -o gateway_tool
    assert "rate_limit.o" in content, "rate_limit.o is missing from the Makefile."

    # Specifically look for it in the gateway_tool target recipe
    lines = content.split('\n')
    linking_line = ""
    for i, line in enumerate(lines):
        if line.startswith("gateway_tool:"):
            if i + 1 < len(lines):
                linking_line = lines[i+1]
            break

    assert "rate_limit.o" in linking_line, "Makefile linking step does not include rate_limit.o"

def test_gateway_tool_compiled():
    exe_path = '/home/user/api_gateway/gateway_tool'
    assert os.path.isfile(exe_path), f"Executable {exe_path} not found. Did the build succeed?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_log_file_contents():
    log_path = '/home/user/gateway_test_results.log'
    assert os.path.isfile(log_path), f"Log file {log_path} was not generated."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in the log file, but found {len(lines)}."

    assert lines[0] == "ALLOWED", f"Line 1 expected ALLOWED, got {lines[0]}"
    assert lines[1] == "CHECKSUM_FAILED", f"Line 2 expected CHECKSUM_FAILED, got {lines[1]}"
    assert lines[2] == "ALLOWED", f"Line 3 expected ALLOWED, got {lines[2]}"
    assert lines[3] == "ALLOWED", f"Line 4 expected ALLOWED, got {lines[3]}"
    # Since the gateway_tool is run as a separate process each time, in-memory rate limiting 
    # will reset. We accept both the logically correct in-memory result (ALLOWED) and the 
    # prompt's literal expected result (RATE_LIMITED) in case the student persisted state.
    assert lines[4] in ["ALLOWED", "RATE_LIMITED"], f"Line 5 expected ALLOWED or RATE_LIMITED, got {lines[4]}"

def test_checksum_logic_via_executable():
    exe_path = '/home/user/api_gateway/gateway_tool'
    if not os.path.isfile(exe_path):
        pytest.skip("gateway_tool not compiled")

    # Test valid checksum (payload_A -> 16223)
    res_valid = subprocess.run([exe_path, '192.168.1.1', 'payload_A', '16223'], capture_output=True, text=True)
    assert "ALLOWED" in res_valid.stdout, f"Expected ALLOWED for valid checksum, got: {res_valid.stdout}"

    # Test invalid checksum
    res_invalid = subprocess.run([exe_path, '192.168.1.2', 'payload_A', '9999'], capture_output=True, text=True)
    assert "CHECKSUM_FAILED" in res_invalid.stdout, f"Expected CHECKSUM_FAILED for invalid checksum, got: {res_invalid.stdout}"