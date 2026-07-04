# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_reproducibility_passes():
    """
    Validates that the vendored package has been fixed to construct the state matrix 
    deterministically, causing the reproducibility test to pass.
    """
    test_file = "/app/mcmc_graph_solver/tests/test_reproducibility.py"
    assert os.path.exists(test_file), f"Test file {test_file} is missing."

    result = subprocess.run(
        ["pytest", test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Reproducibility test failed. The matrix construction is likely still non-deterministic.\nPytest Output:\n{result.stdout}\n{result.stderr}"

def test_adversarial_corpus():
    """
    Validates the agent's graph_filter.py against the clean and evil corpora.
    Clean files must return 0, evil files must return 1.
    """
    script_path = "/home/user/graph_filter.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    clean_failures = []
    for f in clean_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_failures)}")

    assert not error_messages, "Adversarial corpus validation failed:\n" + "\n".join(error_messages)