# test_final_state.py
import os
import subprocess
import pytest

def test_pytest_passes():
    """Verify that the test_server.py tests pass successfully."""
    test_file = "/home/user/ws_asm/test_server.py"
    assert os.path.isfile(test_file), f"Test file {test_file} is missing."

    result = subprocess.run(
        ["pytest", test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest on {test_file} failed:\n{result.stdout}\n{result.stderr}"

def test_response_log_exists():
    """Verify that the response log was generated."""
    log_file = "/home/user/ws_asm/response.log"
    assert os.path.isfile(log_file), f"Response log {log_file} is missing."

def test_response_log_content():
    """Verify that the response log contains the correct machine code for exit(42)."""
    log_file = "/home/user/ws_asm/response.log"
    with open(log_file, "r") as f:
        hex_data = f.read().strip()

    assert hex_data, "Response log is empty."

    try:
        code = bytes.fromhex(hex_data)
    except ValueError:
        pytest.fail("Response log does not contain valid hex-encoded data.")

    # Check for syscall instruction (0f 05)
    assert b'\x0f\x05' in code, "Machine code does not contain a syscall instruction (0f 05)."

    # Check for presence of 42 (0x2a) and 60 (0x3c for sys_exit)
    assert b'\x2a' in code, "Machine code does not contain the value 42 (0x2a)."
    assert b'\x3c' in code, "Machine code does not contain the sys_exit syscall number 60 (0x3c)."