# test_final_state.py

import os
import subprocess
import hashlib
import pytest

BUILD_DIR = "/home/user/build"
AMD64_BIN = os.path.join(BUILD_DIR, "gateway_amd64")
ARM64_BIN = os.path.join(BUILD_DIR, "gateway_arm64")
HASHES_FILE = os.path.join(BUILD_DIR, "hashes.txt")
STRESS_GO = "/home/user/gateway/tests/stress.go"

def test_build_directory_and_binaries_exist():
    assert os.path.isdir(BUILD_DIR), f"Build directory {BUILD_DIR} does not exist."
    assert os.path.isfile(AMD64_BIN), f"Binary {AMD64_BIN} does not exist."
    assert os.path.isfile(ARM64_BIN), f"Binary {ARM64_BIN} does not exist."

def test_amd64_secure_mode():
    # Running without args should exit 0 and NOT print INSECURE
    result = subprocess.run([AMD64_BIN], capture_output=True, text=True)
    assert result.returncode == 0, f"{AMD64_BIN} exited with code {result.returncode}, expected 0."
    assert "INSECURE" not in result.stdout, f"{AMD64_BIN} was not compiled with -DSECURE_MODE."

def test_arm64_architecture():
    # Check if the ARM64 binary is actually aarch64
    result = subprocess.run(["file", ARM64_BIN], capture_output=True, text=True)
    assert "aarch64" in result.stdout.lower() or "arm64" in result.stdout.lower(), \
        f"{ARM64_BIN} does not appear to be an ARM64 binary: {result.stdout}"

def test_urldecode_functionality():
    # Test valid encoding
    res1 = subprocess.run([AMD64_BIN, "hello%20world"], capture_output=True, text=True)
    assert res1.returncode == 0
    assert res1.stdout.strip() == "hello world", f"Failed to decode valid URL: {res1.stdout}"

    # Test incomplete encoding
    res2 = subprocess.run([AMD64_BIN, "incomplete%"], capture_output=True, text=True)
    assert res2.returncode == 0
    assert res2.stdout.strip() == "incomplete%", f"Failed to handle incomplete encoding: {res2.stdout}"

    # Test invalid hex
    res3 = subprocess.run([AMD64_BIN, "invalid%ZZ"], capture_output=True, text=True)
    assert res3.returncode == 0
    assert res3.stdout.strip() == "invalid%ZZ", f"Failed to handle invalid hex encoding: {res3.stdout}"

def test_stress_go_concurrency():
    assert os.path.isfile(STRESS_GO), f"{STRESS_GO} does not exist."
    with open(STRESS_GO, "r") as f:
        content = f.read()

    assert "go " in content, "stress.go does not use goroutines ('go ' keyword missing)."
    assert "sync.WaitGroup" in content or "chan " in content, \
        "stress.go does not use sync.WaitGroup or channels for concurrency synchronization."
    assert "100" in content, "stress.go does not appear to run 100 times."

def test_hashes_file():
    assert os.path.isfile(HASHES_FILE), f"Hashes file {HASHES_FILE} does not exist."
    with open(HASHES_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {HASHES_FILE}, found {len(lines)}."

    content = "\n".join(lines)
    assert "gateway_amd64" in content, "gateway_amd64 missing from hashes.txt"
    assert "gateway_arm64" in content, "gateway_arm64 missing from hashes.txt"

    # Verify hashes
    with open(AMD64_BIN, "rb") as f:
        amd64_hash = hashlib.sha256(f.read()).hexdigest()
    with open(ARM64_BIN, "rb") as f:
        arm64_hash = hashlib.sha256(f.read()).hexdigest()

    assert amd64_hash in content, f"Correct SHA256 for gateway_amd64 ({amd64_hash}) not found in hashes.txt"
    assert arm64_hash in content, f"Correct SHA256 for gateway_arm64 ({arm64_hash}) not found in hashes.txt"