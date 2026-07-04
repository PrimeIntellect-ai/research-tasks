# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_run_eval_script_and_check_results():
    script_path = "/home/user/run_eval.sh"
    assert os.path.isfile(script_path), f"Missing evaluation script at {script_path}"

    # Run the user's evaluation script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_eval.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    results_path = "/home/user/eval_results.txt"
    assert os.path.isfile(results_path), f"Missing evaluation results at {results_path}"

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    results_dict = {}
    for line in lines:
        parts = line.split(" ", 1)
        if len(parts) == 2:
            status, filepath = parts
            results_dict[filepath] = status

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.fasta"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.fasta"))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"

    clean_modified = []
    for cf in clean_files:
        if results_dict.get(cf) != "ACCEPT":
            clean_modified.append(cf)

    evil_bypassed = []
    for ef in evil_files:
        if results_dict.get(ef) != "REJECT":
            evil_bypassed.append(ef)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join(os.path.basename(f) for f in evil_bypassed))
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: " + ", ".join(os.path.basename(f) for f in clean_modified))

    assert not error_msgs, " | ".join(error_msgs)