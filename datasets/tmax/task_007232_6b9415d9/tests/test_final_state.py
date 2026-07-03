# test_final_state.py
import os
import re

def test_profile_out_exists_and_correct():
    out_path = "/home/user/profile_out.txt"
    assert os.path.exists(out_path), f"Output file {out_path} is missing."

    with open(out_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = ["perf_metric_app_1298", "cpu_usage_100_percent"]
    assert content == expected, f"Output file content is incorrect. Expected {expected}, got {content}."

def test_run_profiler_script_fixes():
    script_path = "/home/user/run_profiler.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check if the SQL query was fixed
    assert re.search(r"status\s*=\s*1", content), "The script does not query 'status = 1'."
    assert "status = 'active'" not in content, "The script still contains the buggy SQL query 'status = active'."

    # Check if the hidden flag was added
    assert "--x-decode-v2" in content, "The script does not pass the hidden flag '--x-decode-v2' to the binary."

    # Check if a recursion limit was added
    assert "3" in content, "The script does not seem to contain the attempt limit of 3."