# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_filter_dataset_script_exists():
    """Ensure the user created the required script."""
    script_path = "/home/user/filter_dataset.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_adversarial_corpus_evaluation():
    """
    Evaluate the agent's script against the clean and evil corpora.
    Clean files must output ACCEPT.
    Evil files must output REJECT.
    """
    script_path = "/home/user/filter_dataset.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean CSV files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil CSV files found in {evil_dir}"

    clean_failures = []
    for cf in clean_files:
        try:
            result = subprocess.run(
                ["python", script_path, cf],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_failures.append(os.path.basename(cf))
        except subprocess.TimeoutExpired:
            clean_failures.append(f"{os.path.basename(cf)} (Timeout)")
        except Exception as e:
            clean_failures.append(f"{os.path.basename(cf)} (Error: {e})")

    evil_failures = []
    for ef in evil_files:
        try:
            result = subprocess.run(
                ["python", script_path, ef],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout.strip()
            if output != "REJECT":
                evil_failures.append(os.path.basename(ef))
        except subprocess.TimeoutExpired:
            # A timeout is considered a bypass since it didn't print REJECT
            evil_failures.append(f"{os.path.basename(ef)} (Timeout)")
        except Exception as e:
            evil_failures.append(f"{os.path.basename(ef)} (Error: {e})")

    error_msg = []
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))