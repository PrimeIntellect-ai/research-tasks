# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
BATS_EXEC = "/app/bats-core/bin/bats"

def test_detector_script_exists_and_executable():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"
    assert os.access(DETECTOR_SCRIPT, os.X_OK), f"Detector script {DETECTOR_SCRIPT} is not executable"

def test_bats_core_fixed():
    assert os.path.isfile(BATS_EXEC), f"Bats executable {BATS_EXEC} is missing."

    with open(BATS_EXEC, "r") as f:
        first_line = f.readline().strip()

    assert first_line != "#!/bin/broken-bash", "The shebang in bats-core is still broken."

    # Check if it runs successfully
    try:
        result = subprocess.run([BATS_EXEC, "-v"], capture_output=True, text=True, check=True)
        assert "Bats 1.9.0" in result.stdout, f"Expected 'Bats 1.9.0' in output, got: {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to execute bats-core: {e.stderr}")
    except OSError as e:
        pytest.fail(f"Failed to execute bats-core (OS error): {e}")

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (should be accepted): {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([DETECTOR_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be rejected): {', '.join(failed_files)}")