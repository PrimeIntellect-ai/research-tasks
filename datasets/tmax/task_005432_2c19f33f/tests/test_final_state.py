# test_final_state.py

import os
import subprocess
import pytest

def test_bad_line_txt():
    path = "/home/user/bad_line.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    expected_line = "2023-10-01 12:00:03 [ERROR] \"SELECT * FROM orders WHERE user_id = 12345 AND status = 'pending' AND created_at > '2023-01-01'\""
    assert expected_line in content, f"{path} does not contain the correct offending log line."

def test_fixed_c_compiles_and_runs(tmp_path):
    src_path = "/home/user/log_processor_fixed.c"
    assert os.path.isfile(src_path), f"File {src_path} does not exist."

    exe_path = str(tmp_path / "log_processor_fixed")

    # Compile the fixed C file
    compile_proc = subprocess.run(
        ["gcc", "-o", exe_path, src_path],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr}"

    # Run the compiled executable
    run_proc = subprocess.run(
        [exe_path],
        capture_output=True,
        text=True
    )
    assert run_proc.returncode == 0, f"Execution failed or crashed. Return code: {run_proc.returncode}\nStderr: {run_proc.stderr}"