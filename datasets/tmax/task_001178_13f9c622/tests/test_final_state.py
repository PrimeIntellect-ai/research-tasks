# test_final_state.py

import os
import stat
import pytest

def test_summary_result():
    result_file = "/home/user/deploy/summary_result.txt"
    assert os.path.isfile(result_file), f"Verification file missing: {result_file}"

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content == "4", f"Expected summary_result.txt to contain '4', but found '{content}'"

def test_monitor_script_executable():
    script_file = "/home/user/deploy/scripts/monitor.sh"
    assert os.path.isfile(script_file), f"Monitor script missing: {script_file}"

    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"Monitor script is not executable: {script_file}"

def test_summary_script_executable():
    script_file = "/home/user/deploy/scripts/summary.sh"
    assert os.path.isfile(script_file), f"Summary script missing: {script_file}"

    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"Summary script is not executable: {script_file}"

def test_processed_files():
    out_dir = "/home/user/deploy/data/out/"
    assert os.path.isdir(out_dir), f"Output directory missing: {out_dir}"

    files = [f for f in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, f))]
    assert len(files) >= 4, f"Expected at least 4 processed files in {out_dir}, found {len(files)}"

def test_cpp_code_fixed():
    src_file = "/home/user/deploy/src/processor.cpp"
    assert os.path.isfile(src_file), f"Source file missing: {src_file}"

    with open(src_file, 'r') as f:
        content = f.read()

    assert "std::abort()" not in content, "The C++ code still contains std::abort() which causes crashes."
    assert "WARNING: Poison pill skipped in" in content, "The C++ code does not log the expected warning message."