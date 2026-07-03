# test_final_state.py

import os
import stat
import pytest

def test_fixed_script_exists_and_executable():
    script_path = "/home/user/process_logs_fixed.sh"
    assert os.path.isfile(script_path), f"Fixed script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Fixed script {script_path} is not executable."

def test_fixed_script_contains_parallelization():
    script_path = "/home/user/process_logs_fixed.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "&" in content, "The parallelization logic ('&') was removed from the script."
    assert "wait" in content, "The parallelization logic ('wait') was removed from the script."

def test_final_report_content():
    report_path = "/home/user/final_report.txt"
    assert os.path.isfile(report_path), f"Final report {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "Rate: 62", f"Expected final report to contain 'Rate: 62', but got '{content}'."