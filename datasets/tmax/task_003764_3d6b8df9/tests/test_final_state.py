# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

def test_classifier_accuracy():
    classifier_path = "/home/user/classifier.py"
    assert os.path.isfile(classifier_path), f"Classifier script not found at {classifier_path}"

    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    with tempfile.TemporaryDirectory() as tmpdir:
        clean_out = os.path.join(tmpdir, "clean_out.json")
        evil_out = os.path.join(tmpdir, "evil_out.json")

        # Run on clean corpus
        res_clean = subprocess.run(
            ["python3", classifier_path, clean_dir, clean_out],
            capture_output=True, text=True
        )
        assert res_clean.returncode == 0, f"Classifier failed on clean corpus:\n{res_clean.stderr}"

        # Run on evil corpus
        res_evil = subprocess.run(
            ["python3", classifier_path, evil_dir, evil_out],
            capture_output=True, text=True
        )
        assert res_evil.returncode == 0, f"Classifier failed on evil corpus:\n{res_evil.stderr}"

        assert os.path.isfile(clean_out), "Classifier did not produce output JSON for clean corpus."
        assert os.path.isfile(evil_out), "Classifier did not produce output JSON for evil corpus."

        with open(clean_out, 'r') as f:
            clean_results = json.load(f)

        with open(evil_out, 'r') as f:
            evil_results = json.load(f)

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.log')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.log')]

    clean_modified = []
    for cf in clean_files:
        if clean_results.get(cf) != "clean":
            clean_modified.append(cf)

    evil_bypassed = []
    for ef in evil_files:
        if evil_results.get(ef) != "evil":
            evil_bypassed.append(ef)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_package_fixed():
    # Verify the package can be imported and doesn't crash on empty/malformed lines
    test_script = """
import sys
try:
    from async_log_parser import parse_file
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

# Create a dummy file with a malformed line
with open('dummy.log', 'w') as f:
    f.write('malformed line without separator\\n')
    f.write('10:00:00 - [START] Task 1\\n')

try:
    events = parse_file('dummy.log')
    if len(events) != 2:
        sys.exit(2)
except Exception as e:
    print(f"Crash: {e}")
    sys.exit(3)
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "test_pkg.py")
        with open(script_path, "w") as f:
            f.write(test_script)

        res = subprocess.run(["python3", script_path], cwd=tmpdir, capture_output=True, text=True)
        assert res.returncode == 0, f"Vendored package is still broken or not installed properly:\n{res.stdout}\n{res.stderr}"