# test_final_state.py

import os
import subprocess
import glob

def test_validate_trace_script_exists():
    script_path = "/home/user/validate_trace.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_clean_traces_accepted():
    script_path = "/home/user/validate_trace.sh"
    clean_dir = "/app/traces/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean traces found in {clean_dir}"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        assert False, f"{len(failed_files)} of {len(clean_files)} clean traces rejected (expected to be accepted). Offending files: {', '.join(failed_files)}"

def test_evil_traces_rejected():
    script_path = "/home/user/validate_trace.sh"
    evil_dir = "/app/traces/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, f"No evil traces found in {evil_dir}"

    failed_files = []
    for f in evil_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        assert False, f"{len(failed_files)} of {len(evil_files)} evil traces bypassed (expected to be rejected). Offending files: {', '.join(failed_files)}"