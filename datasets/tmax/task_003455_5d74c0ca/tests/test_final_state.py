# test_final_state.py

import os
import stat
import subprocess
import pytest

def get_expected_word_count():
    data_dir = "/home/user/project/data"
    total = 0
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith(".txt"):
                with open(os.path.join(data_dir, f), "r") as file:
                    total += len(file.read().split())
    return total

def test_py_worker_exists():
    path = "/home/user/project/py_worker.py"
    assert os.path.isfile(path), f"Python worker script is missing: {path}"

def test_test_orchestrator_exists():
    path = "/home/user/project/test_orchestrator.py"
    assert os.path.isfile(path), f"Test orchestrator script is missing: {path}"

def test_linux_binary_exists_and_executable():
    path = "/home/user/project/build/linux/worker"
    assert os.path.isfile(path), f"Linux binary is missing: {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Linux binary is not executable: {path}"

def test_windows_binary_exists():
    path = "/home/user/project/build/windows/worker.exe"
    assert os.path.isfile(path), f"Windows binary is missing: {path}"

def test_test_result_log():
    path = "/home/user/project/test_result.log"
    assert os.path.isfile(path), f"Test result log is missing: {path}"

    expected_count = get_expected_word_count()
    expected_line = f"TEST PASSED: Total words: {expected_count}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert expected_line in content, f"Log file does not contain the expected success message. Found: {content}"

def test_py_worker_execution():
    path = "/home/user/project/py_worker.py"
    data_dir = "/home/user/project/data"

    result = subprocess.run(["python3", path, data_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"py_worker.py failed to execute. stderr: {result.stderr}"

    expected_count = get_expected_word_count()
    expected_output = f"Total words: {expected_count}"

    assert expected_output in result.stdout, f"py_worker.py did not output the expected word count. Output: {result.stdout}"

def test_linux_binary_execution():
    path = "/home/user/project/build/linux/worker"
    data_dir = "/home/user/project/data"

    result = subprocess.run([path, data_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Linux Go binary failed to execute. stderr: {result.stderr}"

    expected_count = get_expected_word_count()
    expected_output = f"Total words: {expected_count}"

    assert expected_output in result.stdout, f"Linux Go binary did not output the expected word count. Output: {result.stdout}"