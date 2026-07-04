# test_final_state.py

import os
import subprocess
import pytest

GATEWAY_DIR = "/home/user/gateway"
BUILD_DIR = os.path.join(GATEWAY_DIR, "build")

def test_tests_pass_fallback():
    """Verify that the tests pass with the fallback tag, indicating the leak and fixture are fixed."""
    result = subprocess.run(
        ["go", "test", "-tags=fallback", "./..."],
        cwd=GATEWAY_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Tests failed for fallback tag:\n{result.stdout}\n{result.stderr}"

def test_tests_pass_fast():
    """Verify that the tests pass with the fast tag."""
    result = subprocess.run(
        ["go", "test", "-tags=fast", "./..."],
        cwd=GATEWAY_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Tests failed for fast tag:\n{result.stdout}\n{result.stderr}"

def test_fast_amd64_binary():
    """Verify the fast amd64 binary exists and has the correct architecture."""
    binary_path = os.path.join(BUILD_DIR, "gateway_fast_amd64")
    assert os.path.isfile(binary_path), f"Missing binary: {binary_path}"

    with open(binary_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{binary_path} is not an ELF binary"
        f.seek(18)
        machine = f.read(2)
        # e_machine for AMD x86-64 is 0x3E (62 in decimal)
        assert machine == b"\x3e\x00", f"Expected AMD64 architecture, got {machine}"

def test_fallback_arm64_binary():
    """Verify the fallback arm64 binary exists and has the correct architecture."""
    binary_path = os.path.join(BUILD_DIR, "gateway_fallback_arm64")
    assert os.path.isfile(binary_path), f"Missing binary: {binary_path}"

    with open(binary_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{binary_path} is not an ELF binary"
        f.seek(18)
        machine = f.read(2)
        # e_machine for AArch64 is 0xB7 (183 in decimal)
        assert machine == b"\xb7\x00", f"Expected ARM64 architecture, got {machine}"