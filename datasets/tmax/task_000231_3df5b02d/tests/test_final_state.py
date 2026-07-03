# test_final_state.py

import os
import stat
import subprocess
import pytest

APP_DIR = "/home/user/app"
KEY_TXT = os.path.join(APP_DIR, "key.txt")
ANALYZER_CPP = os.path.join(APP_DIR, "analyzer.cpp")
TEST_SH = os.path.join(APP_DIR, "test.sh")

def test_key_extracted_correctly():
    assert os.path.exists(KEY_TXT), f"File {KEY_TXT} does not exist."
    assert os.path.isfile(KEY_TXT), f"{KEY_TXT} is not a file."

    with open(KEY_TXT, 'r') as f:
        content = f.read().strip()

    assert content == "TEST_KEY_849302", f"Expected key 'TEST_KEY_849302', but found '{content}' in {KEY_TXT}."

def test_analyzer_cpp_fixed():
    assert os.path.exists(ANALYZER_CPP), f"File {ANALYZER_CPP} does not exist."

    with open(ANALYZER_CPP, 'r') as f:
        content = f.read()

    assert "(1.0 - k)" in content, f"The corrected EMA formula containing '(1.0 - k)' was not found in {ANALYZER_CPP}."
    assert "(1.0 + k)" not in content, f"The buggy EMA formula containing '(1.0 + k)' is still present in {ANALYZER_CPP}."

def test_test_script_exists_and_executable():
    assert os.path.exists(TEST_SH), f"Script {TEST_SH} does not exist."
    assert os.path.isfile(TEST_SH), f"{TEST_SH} is not a file."

    st = os.stat(TEST_SH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{TEST_SH} does not have executable permissions."

def test_test_script_execution():
    # Ensure test.sh exists and is executable before running
    if not os.path.exists(TEST_SH) or not os.access(TEST_SH, os.X_OK):
        pytest.fail(f"Cannot execute {TEST_SH} because it is missing or not executable.")

    # Run the test script
    result = subprocess.run([TEST_SH], cwd=APP_DIR, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"{TEST_SH} failed with exit code {result.returncode}.\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )