# test_final_state.py
import os
import json
import subprocess
import glob
import pytest

def test_detector_script():
    script_path = "/home/user/detector.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

    clean_dir = "/app/test_traces/clean"
    evil_dir = "/app/test_traces/evil"

    clean_out = "/tmp/clean_out.json"
    evil_out = "/tmp/evil_out.json"

    # Run against clean
    res_clean = subprocess.run(
        ["python", script_path, "--input-dir", clean_dir, "--output", clean_out],
        capture_output=True, text=True
    )
    assert res_clean.returncode == 0, f"Script failed on clean traces:\n{res_clean.stderr}"

    # Run against evil
    res_evil = subprocess.run(
        ["python", script_path, "--input-dir", evil_dir, "--output", evil_out],
        capture_output=True, text=True
    )
    assert res_evil.returncode == 0, f"Script failed on evil traces:\n{res_evil.stderr}"

    assert os.path.isfile(clean_out), f"Output JSON not found at {clean_out}"
    assert os.path.isfile(evil_out), f"Output JSON not found at {evil_out}"

    with open(clean_out, 'r') as f:
        clean_results = json.load(f)

    with open(evil_out, 'r') as f:
        evil_results = json.load(f)

    clean_files = [os.path.basename(f) for f in glob.glob(os.path.join(clean_dir, "*.csv"))]
    evil_files = [os.path.basename(f) for f in glob.glob(os.path.join(evil_dir, "*.csv"))]

    clean_failures = []
    for cf in clean_files:
        if clean_results.get(cf) != "clean":
            clean_failures.append(cf)

    evil_failures = []
    for ef in evil_files:
        if evil_results.get(ef) != "evil":
            evil_failures.append(ef)

    err_msg = []
    if clean_failures:
        err_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/flagged as evil: {clean_failures}")
    if evil_failures:
        err_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/flagged as clean: {evil_failures}")

    assert not err_msg, " | ".join(err_msg)