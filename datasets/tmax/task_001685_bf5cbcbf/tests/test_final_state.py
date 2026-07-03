# test_final_state.py
import os
import subprocess
from pathlib import Path

def test_filter_script_exists_and_executable():
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable. Did you run chmod +x?"

def test_adversarial_corpus():
    script_path = "/home/user/filter.sh"
    clean_dir = Path("/app/clean")
    evil_dir = Path("/app/evil")

    assert clean_dir.is_dir(), f"{clean_dir} directory is missing."
    assert evil_dir.is_dir(), f"{evil_dir} directory is missing."

    clean_files = list(clean_dir.iterdir())
    evil_files = list(evil_dir.iterdir())

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([script_path, str(cf)], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(cf.name)

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([script_path, str(ef)], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(ef.name)

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean files failed (expected exit 0, got something else). Offending files: {', '.join(clean_failed[:10])}{'...' if len(clean_failed) > 10 else ''}")

    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil files bypassed (expected exit 1, got something else). Offending files: {', '.join(evil_bypassed[:10])}{'...' if len(evil_bypassed) > 10 else ''}")

    assert not error_messages, " | ".join(error_messages)

def test_no_forbidden_languages():
    script_path = "/home/user/filter.sh"
    with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    forbidden = ["python", "perl", "ruby", "node"]
    for lang in forbidden:
        assert lang not in content.lower(), f"Script appears to use forbidden language: {lang}"