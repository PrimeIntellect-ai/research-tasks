# test_final_state.py
import os
import stat
import pytest

def test_build_and_run_script_executable():
    script_path = "/home/user/waf_pipeline/build_and_run.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"The script {script_path} is not executable."

def test_scan_result_log():
    log_path = "/home/user/waf_pipeline/scan_result.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist. Did the pipeline run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Recompute the expected value: 42 ^ 15
    expected_val = 42 ^ 15
    expected_str = f"RESULT: [{expected_val}]"

    assert content == expected_str, f"Expected log file to contain '{expected_str}', but got '{content}'."