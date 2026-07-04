# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_card_count():
    card_count_path = "/home/user/card_count.txt"
    assert os.path.isfile(card_count_path), f"File {card_count_path} does not exist."
    with open(card_count_path, "r") as f:
        content = f.read().strip()
    assert content == "7", f"Expected card count to be 7, but got '{content}'."

def test_sanitize_script_adversarial_corpus():
    script_path = "/home/user/sanitize.py"
    assert os.path.isfile(script_path), f"Sanitize script {script_path} does not exist."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_bypassed = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean corpus
        for c_file in clean_files:
            out_file = os.path.join(tmpdir, os.path.basename(c_file) + "_out")
            subprocess.run(["python3", script_path, c_file, out_file], check=False)
            if not os.path.isfile(out_file):
                clean_bypassed.append(os.path.basename(c_file))
                continue
            with open(c_file, "r") as f1, open(out_file, "r") as f2:
                if f1.read() != f2.read():
                    clean_bypassed.append(os.path.basename(c_file))

        # Test evil corpus
        for e_file in evil_files:
            out_file = os.path.join(tmpdir, os.path.basename(e_file) + "_out")
            subprocess.run(["python3", script_path, e_file, out_file], check=False)
            if os.path.isfile(out_file):
                with open(out_file, "r") as f:
                    content = f.read()
                if content.strip() != "":
                    evil_bypassed.append(os.path.basename(e_file))

    errors = []
    if clean_bypassed:
        errors.append(f"{len(clean_bypassed)} of {len(clean_files)} clean modified: {', '.join(clean_bypassed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, "Adversarial corpus validation failed: " + "; ".join(errors)

def test_pipeline_script_and_cron():
    pipeline_script = "/home/user/run_pipeline.sh"
    assert os.path.isfile(pipeline_script), f"Pipeline script {pipeline_script} does not exist."
    assert os.access(pipeline_script, os.X_OK), f"Pipeline script {pipeline_script} is not executable."

    # Check cron job
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    cron_output = result.stdout
    assert "*/5 * * * *" in cron_output and "run_pipeline.sh" in cron_output, "Cron job for run_pipeline.sh with schedule */5 * * * * not found."

def test_pipeline_execution():
    pipeline_script = "/home/user/run_pipeline.sh"

    # Remove files if they exist to test creation
    files_to_check = [
        "/home/user/pipeline.log",
        "/home/user/card_count.txt",
        "/home/user/final_translations.txt"
    ]
    for f in files_to_check:
        if os.path.exists(f):
            os.remove(f)

    # Run the pipeline script
    result = subprocess.run(["bash", pipeline_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script execution failed with output: {result.stderr}"

    for f in files_to_check:
        assert os.path.isfile(f), f"Expected file {f} was not created by the pipeline script."
        assert os.path.getsize(f) > 0, f"File {f} is empty."