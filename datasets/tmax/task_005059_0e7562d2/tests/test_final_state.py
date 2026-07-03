# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_filter_py_exists():
    assert os.path.exists("/home/user/filter.py"), "Missing /home/user/filter.py script."

def test_report_exists():
    assert os.path.exists("/home/user/report.txt"), "Missing /home/user/report.txt. Ensure the ETL pipeline and modeling step completed."
    assert os.path.getsize("/home/user/report.txt") > 0, "/home/user/report.txt is empty."

def test_filter_clean_corpus():
    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."

    modified_clean = []
    for f in clean_files:
        result = subprocess.run(["python3", "/home/user/filter.py", f], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(f))

    if modified_clean:
        pytest.fail(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected instead of preserved): {', '.join(modified_clean)}")

def test_filter_evil_corpus():
    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    bypassed_evil = []
    for f in evil_files:
        result = subprocess.run(["python3", "/home/user/filter.py", f], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(f))

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(bypassed_evil)}")