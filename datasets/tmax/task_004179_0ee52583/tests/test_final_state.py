# test_final_state.py
import os
import subprocess
import pytest

def test_filter_script_exists():
    assert os.path.isfile("/home/user/filter.py"), "Missing filter script: /home/user/filter.py"

def test_adversarial_corpus():
    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"
    script = "/home/user/filter.py"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])
    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])

    clean_modified = []
    evil_bypassed = []

    # Test clean corpus (should exit 0)
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, "rb") as stdin_f:
            res = subprocess.run(["python3", script], stdin=stdin_f, capture_output=True)
            if res.returncode != 0:
                clean_modified.append(f)

    # Test evil corpus (should exit non-zero)
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, "rb") as stdin_f:
            res = subprocess.run(["python3", script], stdin=stdin_f, capture_output=True)
            if res.returncode == 0:
                evil_bypassed.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))