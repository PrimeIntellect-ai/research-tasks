# test_final_state.py

import os
import stat
import pytest

BASE_DIR = "/home/user/system_check"
SCRIPT_PATH = "/home/user/build_and_test.sh"
LOG_PATH = "/home/user/test_results.log"

def test_patch_applied_libcore():
    filepath = os.path.join(BASE_DIR, "libcore.c")
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    with open(filepath, "r") as f:
        content = f.read()
    assert "free(ptr);" in content, "The memory leak in libcore.c was not fixed (patch not applied properly)."

def test_patch_applied_rust():
    filepath = os.path.join(BASE_DIR, "rust_app", "src", "main.rs")
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    with open(filepath, "r") as f:
        content = f.read()
    assert "fn process_data(input: i64) -> i64;" in content, "The ABI signature in main.rs was not updated (patch not applied properly)."
    assert "process_data(21i64)" in content, "The function call in main.rs was not updated (patch not applied properly)."

def test_stress_test_go_fixed():
    filepath = os.path.join(BASE_DIR, "stress_test.go")
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    with open(filepath, "r") as f:
        content = f.read()
    assert "close(results)" in content, "stress_test.go does not contain 'close(results)'. The deadlock was not fixed."

def test_build_and_test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_test_results_log():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist. Did the script run successfully and redirect output?"
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()
    assert content == "All workers completed successfully", f"Log file content is incorrect. Expected 'All workers completed successfully', got '{content}'."