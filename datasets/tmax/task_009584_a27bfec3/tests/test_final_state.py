# test_final_state.py
import os
import stat

def test_mre_input_file():
    mre_path = "/home/user/mre_input.txt"
    assert os.path.exists(mre_path), f"MRE file {mre_path} does not exist."
    assert os.path.isfile(mre_path), f"{mre_path} is not a file."

    with open(mre_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 10, f"Expected exactly 10 lines in {mre_path}, found {len(lines)}."
    for i, line in enumerate(lines):
        assert line.strip() == "50", f"Line {i+1} in {mre_path} is '{line.strip()}', expected '50'."

def test_fixed_c_file():
    fixed_c_path = "/home/user/latency_monitor_fixed.c"
    assert os.path.exists(fixed_c_path), f"Fixed C file {fixed_c_path} does not exist."
    assert os.path.isfile(fixed_c_path), f"{fixed_c_path} is not a file."

    with open(fixed_c_path, "r") as f:
        content = f.read()

    # The bug was sorting 1000 elements instead of `count`
    # We expect `qsort(..., count, ...)` or similar logic
    assert "qsort(latencies, count" in content.replace(" ", ""), \
        f"Could not find the corrected qsort call using 'count' in {fixed_c_path}."

def test_executable_exists():
    exe_path = "/home/user/monitor_fixed"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_fixed_output_log():
    log_path = "/home/user/fixed_output.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_output = "Count: 10, P99 Latency: 50"
    assert expected_output in content, \
        f"Expected '{expected_output}' in {log_path}, but found: '{content}'"