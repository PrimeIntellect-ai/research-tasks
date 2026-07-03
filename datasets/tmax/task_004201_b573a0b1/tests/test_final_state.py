# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist_and_executable():
    assert os.path.isfile("/home/user/sorter.py"), "/home/user/sorter.py is missing"
    assert os.path.isfile("/home/user/test_sorter.py"), "/home/user/test_sorter.py is missing"

    organize_sh = "/home/user/organize.sh"
    assert os.path.isfile(organize_sh), f"{organize_sh} is missing"
    assert os.access(organize_sh, os.X_OK), f"{organize_sh} is not executable"

def test_test_status_log():
    log_path = "/home/user/test_status.log"
    assert os.path.isfile(log_path), f"Test status log missing at {log_path}"

    with open(log_path, "r") as f:
        content = f.read()
    assert "TESTS_PASSED_SUCCESSFULLY" in content, f"'TESTS_PASSED_SUCCESSFULLY' not found in {log_path}"

def test_wrapper_go_cross_compilation():
    bin_path = "/home/user/bin/sorter_bin"
    if os.path.exists(bin_path):
        os.remove(bin_path)

    env = os.environ.copy()
    env["USE_LANG"] = "go"
    env["TARGET_ARCH"] = "arm64"

    target_dir = "/home/user/data/raw_files"
    result = subprocess.run(
        ["/home/user/organize.sh", target_dir],
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"organize.sh failed with USE_LANG=go. Stderr: {result.stderr}"

    assert os.path.isfile(bin_path), f"Go binary not cross-compiled to {bin_path}"

    file_cmd = subprocess.run(["file", bin_path], capture_output=True, text=True)
    assert "ARM aarch64" in file_cmd.stdout, f"Go binary was not cross-compiled for arm64. file output: {file_cmd.stdout}"

def test_wrapper_python_execution():
    test_dir = "/home/user/data/test_py"
    os.makedirs(test_dir, exist_ok=True)

    # Create test files
    open(os.path.join(test_dir, "a.txt"), "w").close()
    open(os.path.join(test_dir, "b.log"), "w").close()
    open(os.path.join(test_dir, "c.tmp"), "w").close()

    env = os.environ.copy()
    env["USE_LANG"] = "python"

    result = subprocess.run(
        ["/home/user/organize.sh", test_dir],
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"organize.sh failed with USE_LANG=python. Stderr: {result.stderr}"

    assert os.path.isfile(os.path.join(test_dir, "text", "a.txt")), "Python script failed to move .txt file to text/ subdirectory"
    assert os.path.isfile(os.path.join(test_dir, "logs", "b.log")), "Python script failed to move .log file to logs/ subdirectory"
    assert not os.path.exists(os.path.join(test_dir, "c.tmp")), "Python script failed to delete .tmp file"