# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_sim_executable():
    sim_exec = "/app/simkit-1.2/sim"
    assert os.path.exists(sim_exec), f"Executable {sim_exec} was not built."
    assert os.access(sim_exec, os.X_OK), f"File {sim_exec} is not executable."

def test_classifier_script_exists():
    script = "/home/user/classifier.sh"
    assert os.path.exists(script), f"Script {script} does not exist."
    assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_classifier_accuracy():
    script = "/home/user/classifier.sh"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = sorted(glob.glob(os.path.join(clean_dir, "*.txt")))
    evil_files = sorted(glob.glob(os.path.join(evil_dir, "*.txt")))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for f in clean_files:
        res = subprocess.run([script, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run([script, f], capture_output=True)
        # We expect exit code 1 for evil files
        if res.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))