# test_final_state.py
import os
import subprocess
import pytest

def test_crash_path_extracted():
    path_file = "/home/user/crash_path.txt"
    assert os.path.isfile(path_file), f"Missing required file: {path_file}"

    with open(path_file, "r") as f:
        content = f.read().strip()

    expected_path = "/api/v1/trigger_leak_992"
    assert content == expected_path, f"Expected {path_file} to contain '{expected_path}', but got '{content}'"

def test_flag_extracted():
    flag_file = "/home/user/flag.txt"
    assert os.path.isfile(flag_file), f"Missing required file: {flag_file}"

    with open(flag_file, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG_{m3m0ry_t4sk_l34k_f0und}"
    assert content == expected_flag, f"Expected {flag_file} to contain '{expected_flag}', but got '{content}'"

def test_build_passes_without_leaks():
    test_script = "/home/user/test_build.py"
    assert os.path.isfile(test_script), f"Missing required file: {test_script}"

    result = subprocess.run(
        ["python3", test_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Expected test_build.py to exit with code 0, but got {result.returncode}. Output: {result.stdout}\n{result.stderr}"
    assert "PASS" in result.stdout, f"Expected 'PASS' in output, but got: {result.stdout}"
    assert "FAIL" not in result.stdout, f"Expected no failures in output, but got: {result.stdout}"