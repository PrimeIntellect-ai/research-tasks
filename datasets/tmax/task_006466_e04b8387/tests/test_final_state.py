# test_final_state.py
import os
import subprocess
import re
import pytest

def test_run_log_output():
    log_path = "/home/user/project/run.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "ataDterceSrepuSHASH", f"Expected 'ataDterceSrepuSHASH' in run.log, but got '{content}'."

def test_fasthash_c_fixed():
    c_file = "/home/user/project/c/fasthash.c"
    assert os.path.isfile(c_file), f"File {c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    # Check if malloc allocates at least len + 5 or strlen(input) + 5
    # Look for malloc(.*+\s*5.*) or similar
    match = re.search(r'malloc\s*\([^)]*\+\s*5\s*\)', content)
    assert match is not None, "fasthash.c does not appear to allocate 'len + 5' (or similar) in malloc."

def test_amd64_binaries():
    app_amd64 = "/home/user/project/bin/app-amd64"
    lib_amd64 = "/home/user/project/lib/amd64/libfasthash.so"

    assert os.path.isfile(app_amd64), f"File {app_amd64} is missing."
    assert os.path.isfile(lib_amd64), f"File {lib_amd64} is missing."

    # Check app architecture
    out = subprocess.run(["file", app_amd64], capture_output=True, text=True).stdout
    assert "ELF 64-bit LSB executable" in out and "x86-64" in out, f"{app_amd64} is not an x86-64 ELF executable."

    # Check lib architecture
    out = subprocess.run(["file", lib_amd64], capture_output=True, text=True).stdout
    assert "ELF 64-bit LSB shared object" in out and "x86-64" in out, f"{lib_amd64} is not an x86-64 ELF shared object."

def test_arm64_binaries():
    app_arm64 = "/home/user/project/bin/app-arm64"
    lib_arm64 = "/home/user/project/lib/arm64/libfasthash.so"

    assert os.path.isfile(app_arm64), f"File {app_arm64} is missing."
    assert os.path.isfile(lib_arm64), f"File {lib_arm64} is missing."

    # Check app architecture
    out = subprocess.run(["file", app_arm64], capture_output=True, text=True).stdout
    assert "ELF 64-bit LSB executable" in out and "aarch64" in out, f"{app_arm64} is not an ARM aarch64 ELF executable."

    # Check lib architecture
    out = subprocess.run(["file", lib_arm64], capture_output=True, text=True).stdout
    assert "ELF 64-bit LSB shared object" in out and "aarch64" in out, f"{lib_arm64} is not an ARM aarch64 ELF shared object."