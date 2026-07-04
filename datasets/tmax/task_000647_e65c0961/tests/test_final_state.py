# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_keygen_c_exists():
    path = "/home/user/keygen.c"
    assert os.path.isfile(path), f"Missing file: {path}"

def test_keygen_executable_and_output():
    path = "/home/user/keygen"
    assert os.path.isfile(path), f"Missing file: {path}"

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

    # Run and check output
    try:
        result = subprocess.run([path, "84729"], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        assert output == "1475851637", f"Expected output '1475851637', got '{output}'"
    except Exception as e:
        pytest.fail(f"Failed to run {path}: {e}")

def test_attacker_token_txt():
    path = "/home/user/attacker_token.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "1475851637", f"Expected token '1475851637', got '{content}'"

def test_block_attacker_sh():
    path = "/home/user/block_attacker.sh"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_command = "iptables -A INPUT -s 203.0.113.42 -j DROP"
    # Filter out shebang or empty lines
    commands = [line for line in lines if not line.startswith("#")]

    assert any(cmd == expected_command for cmd in commands), (
        f"Expected command '{expected_command}' not found in {path}. "
        f"Found commands: {commands}"
    )