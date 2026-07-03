# test_final_state.py

import os
import subprocess
import pytest
import tempfile

VENDORED_SCRIPT = "/app/vendored/bash-datakit/validate_csv.sh"
DETECTOR_SCRIPT = "/home/user/detector.sh"
CLEAN_DIR = "/app/data/clean/"
EVIL_DIR = "/app/data/evil/"

def test_vendored_script_fixed():
    assert os.path.isfile(VENDORED_SCRIPT), f"Vendored script missing: {VENDORED_SCRIPT}"
    with open(VENDORED_SCRIPT, "r") as f:
        content = f.read()
    assert 'print ""' not in content, "Vendored script still contains the bug 'print \"\"'"
    assert 'print $0' in content or 'print' in content, "Vendored script should print the whole line"

def test_detector_script_exists_and_executable():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script missing: {DETECTOR_SCRIPT}"
    assert os.access(DETECTOR_SCRIPT, os.X_OK), f"Detector script is not executable: {DETECTOR_SCRIPT}"

def test_adversarial_corpus():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith(".csv")]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith(".csv")]

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}"

    clean_modified = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean corpus
        for cfile in clean_files:
            out_file = os.path.join(tmpdir, "out_clean_" + os.path.basename(cfile))
            result = subprocess.run([DETECTOR_SCRIPT, cfile, out_file], capture_output=True, text=True)
            if result.returncode != 0:
                clean_modified.append((os.path.basename(cfile), "Script failed with non-zero exit code"))
                continue

            if not os.path.exists(out_file):
                clean_modified.append((os.path.basename(cfile), "Output file not created"))
                continue

            with open(cfile, "r") as f:
                original_lines = [line.strip() for line in f if line.strip()]
            with open(out_file, "r") as f:
                output_lines = [line.strip() for line in f if line.strip()]

            if original_lines != output_lines:
                clean_modified.append((os.path.basename(cfile), f"Expected {len(original_lines)} lines, got {len(output_lines)} lines"))

        # Test evil corpus
        for efile in evil_files:
            out_file = os.path.join(tmpdir, "out_evil_" + os.path.basename(efile))
            result = subprocess.run([DETECTOR_SCRIPT, efile, out_file], capture_output=True, text=True)
            if result.returncode != 0:
                evil_bypassed.append((os.path.basename(efile), "Script failed with non-zero exit code"))
                continue

            if not os.path.exists(out_file):
                evil_bypassed.append((os.path.basename(efile), "Output file not created"))
                continue

            with open(efile, "r") as f:
                original_lines = [line.strip() for line in f if line.strip()]

            with open(out_file, "r") as f:
                output_lines = [line.strip() for line in f if line.strip()]

            # Expected output for evil is just the header
            if len(output_lines) != 1 or output_lines[0] != original_lines[0]:
                evil_bypassed.append((os.path.basename(efile), f"Expected 1 header line, got {len(output_lines)} lines"))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join([f"{f[0]} ({f[1]})" for f in evil_bypassed]))
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: " + ", ".join([f"{f[0]} ({f[1]})" for f in clean_modified]))

    if error_messages:
        pytest.fail(" | ".join(error_messages))