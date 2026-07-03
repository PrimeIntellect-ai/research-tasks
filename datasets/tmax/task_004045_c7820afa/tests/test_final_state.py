# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import filecmp
import pytest

EVIL_DIR = "/app/test_data/corpora/evil"
CLEAN_DIR = "/app/test_data/corpora/clean"
SCRIPT_PATH = "/home/user/sanitize_ts.py"
REFERENCE_CSV = "/app/test_data/reference.csv"

def test_sanitize_ts_adversarial_corpus():
    """
    Test the data sanitization script against the adversarial corpus.
    It must reject all evil files and preserve all clean files exactly.
    """
    assert os.path.isfile(SCRIPT_PATH), f"Sanitization script is missing at {SCRIPT_PATH}"
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory {EVIL_DIR} is missing."
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory {CLEAN_DIR} is missing."
    assert os.path.isfile(REFERENCE_CSV), f"Reference CSV {REFERENCE_CSV} is missing."

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        # Prepare combined input directory
        for f in evil_files:
            shutil.copy2(os.path.join(EVIL_DIR, f), os.path.join(input_dir, f))
        for f in clean_files:
            shutil.copy2(os.path.join(CLEAN_DIR, f), os.path.join(input_dir, f))

        # Run the student's script
        cmd = [
            "python3", SCRIPT_PATH,
            "--input-dir", input_dir,
            "--output-dir", output_dir,
            "--reference", REFERENCE_CSV
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        output_files = set(os.listdir(output_dir))

        # Check for evil files that bypassed the filter
        evil_bypassed = [f for f in evil_files if f in output_files]

        # Check for clean files that were dropped or modified
        clean_missing = [f for f in clean_files if f not in output_files]
        clean_modified = []

        for f in clean_files:
            if f in output_files:
                original_path = os.path.join(CLEAN_DIR, f)
                output_path = os.path.join(output_dir, f)
                if not filecmp.cmp(original_path, output_path, shallow=False):
                    clean_modified.append(f)

        errors = []
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_missing:
            errors.append(f"{len(clean_missing)} of {len(clean_files)} clean missing: {', '.join(clean_missing)}")
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

        assert not errors, " | ".join(errors)