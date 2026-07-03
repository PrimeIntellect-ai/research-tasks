# test_final_state.py

import os
import subprocess
import re

def test_bypass_payload():
    payload_path = "/home/user/bypass_payload.txt"
    assert os.path.exists(payload_path), f"{payload_path} does not exist"

    with open(payload_path, "r") as f:
        payload = f.read().strip()

    assert len(payload) == 10, f"Payload '{payload}' length is not 10 (length is {len(payload)})"
    assert payload.startswith("TST_"), f"Payload '{payload}' does not start with 'TST_'"

    sum_digits = sum(int(c) for c in payload if c.isdigit())
    assert sum_digits == 10, f"Sum of digits in payload '{payload}' is {sum_digits}, expected 10"

def test_tester_arm64_binary():
    binary_path = "/home/user/tester_arm64"
    assert os.path.exists(binary_path), f"{binary_path} does not exist"

    result = subprocess.run(["file", binary_path], capture_output=True, text=True)
    assert "ARM aarch64" in result.stdout, f"{binary_path} is not an ARM aarch64 binary. file output: {result.stdout}"

def test_tester_amd64_binary():
    binary_path = "/home/user/tester_amd64.exe"
    assert os.path.exists(binary_path), f"{binary_path} does not exist"

    result = subprocess.run(["file", binary_path], capture_output=True, text=True)
    assert "PE32+" in result.stdout and "x86-64" in result.stdout, f"{binary_path} is not a Windows AMD64 binary. file output: {result.stdout}"

def test_build_tags():
    tester_dir = "/home/user/tester"
    assert os.path.exists(tester_dir) and os.path.isdir(tester_dir), f"{tester_dir} directory does not exist"

    go_files = [f for f in os.listdir(tester_dir) if f.endswith(".go")]
    assert len(go_files) > 0, f"No .go files found in {tester_dir}"

    has_linux_tag = False
    has_windows_tag = False

    linux_pattern = re.compile(r'//\s*go:build\s+.*linux|//\s*\+build\s+.*linux')
    windows_pattern = re.compile(r'//\s*go:build\s+.*windows|//\s*\+build\s+.*windows')

    for go_file in go_files:
        with open(os.path.join(tester_dir, go_file), "r") as f:
            content = f.read()
            if linux_pattern.search(content):
                has_linux_tag = True
            if windows_pattern.search(content):
                has_windows_tag = True

    assert has_linux_tag, "No Go source file contains a Linux build tag"
    assert has_windows_tag, "No Go source file contains a Windows build tag"