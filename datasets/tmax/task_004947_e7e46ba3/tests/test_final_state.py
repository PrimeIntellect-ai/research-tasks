# test_final_state.py
import os
import subprocess
import re
import pytest

APP_DIR = "/home/user/app"

def test_generate_limits_fixed():
    """Verify that generate_limits.py correctly handles minimums and sorting."""
    limits_rs_path = os.path.join(APP_DIR, "src", "limits.rs")
    assert os.path.isfile(limits_rs_path), "src/limits.rs is missing."

    with open(limits_rs_path, "r") as f:
        content = f.read()

    # Extract all match arms
    arms = re.findall(r'"(/api/v[^"]+)"\s*=>\s*Some\((\d+)\)', content)

    expected_arms = [
        ("/api/v1/admin", 5),
        ("/api/v1/posts", 50),
        ("/api/v1/users", 80),
        ("/api/v2/comments", 200),
        ("/api/v2/tags", 500),
        ("/api/v3/status", 1000)
    ]

    actual_arms = [(path, int(limit)) for path, limit in arms]

    assert actual_arms == expected_arms, f"Expected match arms {expected_arms}, but got {actual_arms}. Check sorting and minimum logic."

def test_unit_test_exists_and_passes():
    """Verify test_generate.py exists and passes."""
    test_file = os.path.join(APP_DIR, "test_generate.py")
    assert os.path.isfile(test_file), "test_generate.py is missing."

    result = subprocess.run(["python3", "-m", "unittest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"test_generate.py failed to run or tests failed:\n{result.stderr}\n{result.stdout}"

def test_cargo_build_succeeds():
    """Verify the Rust project compiles successfully."""
    result = subprocess.run(["cargo", "build"], cwd=APP_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"cargo build failed:\n{result.stderr}"

def test_peak_memory_file():
    """Verify peak_memory.txt exists and contains an integer."""
    mem_file = os.path.join(APP_DIR, "peak_memory.txt")
    assert os.path.isfile(mem_file), "peak_memory.txt is missing."

    with open(mem_file, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"peak_memory.txt does not contain a valid integer: '{content}'"

def test_limits_diff_exists_and_valid():
    """Verify limits.diff exists and looks like a unified diff."""
    diff_file = os.path.join(APP_DIR, "limits.diff")
    assert os.path.isfile(diff_file), "limits.diff is missing."

    with open(diff_file, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, "limits.diff does not appear to be a unified diff."
    assert "get_limit" in content, "limits.diff does not contain expected diff content."