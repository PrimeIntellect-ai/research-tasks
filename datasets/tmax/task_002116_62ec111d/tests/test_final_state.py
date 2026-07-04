# test_final_state.py

import os
import stat
import subprocess
import json
import time

def test_build_cross_script():
    script_path = "/home/user/build_cross.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the build script
    result = subprocess.run([script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"build_cross.sh failed with output:\n{result.stderr}\n{result.stdout}"

def test_compiled_binaries():
    linux_bin = "/home/user/metrics-api/api-linux-amd64"
    windows_bin = "/home/user/metrics-api/api-windows-amd64.exe"

    assert os.path.exists(linux_bin), f"{linux_bin} was not created."
    assert os.path.exists(windows_bin), f"{windows_bin} was not created."

    # Check file types
    linux_file_output = subprocess.run(["file", linux_bin], capture_output=True, text=True).stdout
    assert "ELF 64-bit" in linux_file_output, f"{linux_bin} is not an ELF 64-bit executable."

    windows_file_output = subprocess.run(["file", windows_bin], capture_output=True, text=True).stdout
    assert "PE32+" in windows_file_output and "Windows" in windows_file_output, f"{windows_bin} is not a Windows PE32+ executable."

def test_test_api_script():
    script_path = "/home/user/test_api.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the test script
    result = subprocess.run([script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"test_api.sh failed with output:\n{result.stderr}\n{result.stdout}"

def test_log_file_contents():
    log_file = "/home/user/metrics-api/linux_jobs.log"
    assert os.path.exists(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    expected_lines = [
        "[LINUX] Platform: ios, Job: 101",
        "[LINUX] Platform: android, Job: 201",
        "[LINUX] Platform: ios, Job: 102"
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in {log_file}."

def test_ios_summary_json():
    summary_file = "/home/user/ios_summary.json"
    assert os.path.exists(summary_file), f"{summary_file} does not exist."

    with open(summary_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_file} does not contain valid JSON."

    assert data.get("job_count") == 2, f"Expected job_count to be 2, got {data.get('job_count')}."
    assert data.get("total_duration") == 165, f"Expected total_duration to be 165, got {data.get('total_duration')}."

def test_go_build_tags():
    linux_logger = "/home/user/metrics-api/logger_linux.go"
    windows_logger = "/home/user/metrics-api/logger_windows.go"

    assert os.path.exists(linux_logger), f"{linux_logger} does not exist."
    assert os.path.exists(windows_logger), f"{windows_logger} does not exist."

    with open(linux_logger, "r") as f:
        linux_content = f.read()
        assert "//go:build linux" in linux_content, f"//go:build linux tag missing in {linux_logger}."

    with open(windows_logger, "r") as f:
        windows_content = f.read()
        assert "//go:build windows" in windows_content, f"//go:build windows tag missing in {windows_logger}."