# test_final_state.py
import os
import glob
import subprocess

def test_filter_script_exists():
    assert os.path.isfile("/home/user/filter.py"), "The script /home/user/filter.py does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/filter.py"

    clean_files = glob.glob("/var/opt/clean_corpus/*.jsonl")
    evil_files = glob.glob("/var/opt/evil_corpus/*.jsonl")

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_modified = []
    for cf in clean_files:
        result = subprocess.run(
            ["python3", script_path, cf],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_modified.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run(
            ["python3", script_path, ef],
            capture_output=True,
            text=True
        )
        if result.returncode != 1 or result.stdout.strip() != "EVIL":
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        assert False, " | ".join(errors)