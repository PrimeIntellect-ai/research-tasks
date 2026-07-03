# test_final_state.py

import os
import subprocess
import pytest

def test_cracked_pin():
    pin_file = "/home/user/cracked_pin.txt"
    assert os.path.exists(pin_file), f"Expected file {pin_file} does not exist."

    with open(pin_file, "r") as f:
        pin = f.read().strip()

    assert pin == "7482", f"Incorrect PIN. Expected '7482', got '{pin}'."

def test_path_filter_binary_exists():
    binary_file = "/home/user/path_filter"
    assert os.path.exists(binary_file), f"Compiled binary {binary_file} does not exist."
    assert os.access(binary_file, os.X_OK), f"File {binary_file} is not executable."

def test_adversarial_corpus():
    binary_file = "/home/user/path_filter"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.exists(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_failed = []
    clean_total = 0
    for filename in sorted(os.listdir(clean_dir)):
        filepath = os.path.join(clean_dir, filename)
        if os.path.isfile(filepath):
            clean_total += 1
            with open(filepath, "r") as f:
                content = f.read()

            try:
                res = subprocess.run([binary_file, content], capture_output=True, timeout=2)
                if res.returncode != 0:
                    clean_failed.append(filename)
            except Exception as e:
                clean_failed.append(filename)

    evil_failed = []
    evil_total = 0
    for filename in sorted(os.listdir(evil_dir)):
        filepath = os.path.join(evil_dir, filename)
        if os.path.isfile(filepath):
            evil_total += 1
            with open(filepath, "r") as f:
                content = f.read()

            try:
                res = subprocess.run([binary_file, content], capture_output=True, timeout=2)
                if res.returncode != 1:
                    evil_failed.append(filename)
            except Exception as e:
                evil_failed.append(filename)

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {evil_total} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {clean_total} clean modified: {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))