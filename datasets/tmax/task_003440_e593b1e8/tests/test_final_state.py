# test_final_state.py

import os
import subprocess
import pytest
import glob

def test_mathlib_compiled():
    so_path = "/home/user/mathlib/libmathparser.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled."

def test_validator_script_exists():
    script_path = "/home/user/validator.py"
    assert os.path.isfile(script_path), f"Validator script {script_path} does not exist."

def test_adversarial_corpus_evaluation():
    script_path = "/home/user/validator.py"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for cf in clean_files:
        try:
            result = subprocess.run(
                ["python3", script_path, "check", cf],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failures.append((os.path.basename(cf), output))
        except Exception as e:
            clean_failures.append((os.path.basename(cf), str(e)))

    evil_failures = []
    for ef in evil_files:
        try:
            result = subprocess.run(
                ["python3", script_path, "check", ef],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failures.append((os.path.basename(ef), output))
        except Exception as e:
            evil_failures.append((os.path.basename(ef), str(e)))

    error_messages = []
    if clean_failures:
        basenames = [f[0] for f in clean_failures]
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(basenames)}")
    if evil_failures:
        basenames = [f[0] for f in evil_failures]
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(basenames)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))