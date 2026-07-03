# test_final_state.py

import os
import json
import subprocess
import sys
import pytest

def test_annoy_installed_and_working():
    """
    Verifies that the annoy package was properly fixed, compiled, and installed.
    """
    try:
        from annoy import AnnoyIndex
        idx = AnnoyIndex(128, 'angular')
    except ImportError as e:
        pytest.fail(f"Failed to import AnnoyIndex. The package might not be installed correctly: {e}")
    except Exception as e:
        pytest.fail(f"Failed to instantiate AnnoyIndex. The C-extension might be broken: {e}")

def test_index_file_exists():
    """
    Verifies that the agent built and saved the Annoy index to the correct location.
    """
    index_path = "/home/user/test_index.ann"
    assert os.path.isfile(index_path), f"The test set index file is missing at {index_path}"
    assert os.path.getsize(index_path) > 0, f"The test set index file at {index_path} is empty"

def test_detector_script_against_corpora():
    """
    Verifies the detector script correctly flags evil files and accepts clean files.
    """
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script not found at {detector_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_out = "/tmp/clean_output.json"
    evil_out = "/tmp/evil_output.json"

    # Run detector on clean corpus
    try:
        subprocess.run([sys.executable, detector_path, clean_dir, clean_out], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Detector script failed when processing clean corpus:\n{e.stderr}")

    # Run detector on evil corpus
    try:
        subprocess.run([sys.executable, detector_path, evil_dir, evil_out], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Detector script failed when processing evil corpus:\n{e.stderr}")

    assert os.path.isfile(clean_out), f"Output JSON log not created at {clean_out}"
    assert os.path.isfile(evil_out), f"Output JSON log not created at {evil_out}"

    with open(clean_out, "r") as f:
        try:
            clean_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {clean_out}")

    with open(evil_out, "r") as f:
        try:
            evil_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {evil_out}")

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_modified = []
    for f in clean_files:
        if f not in clean_results:
            clean_modified.append(f"{os.path.basename(f)} (missing in output)")
        elif clean_results[f] is not True:
            clean_modified.append(f"{os.path.basename(f)} (falsely rejected)")

    evil_bypassed = []
    for f in evil_files:
        if f not in evil_results:
            evil_bypassed.append(f"{os.path.basename(f)} (missing in output)")
        elif evil_results[f] is not False:
            evil_bypassed.append(f"{os.path.basename(f)} (falsely accepted)")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_bypassed))
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: " + ", ".join(clean_modified))

    if errors:
        pytest.fail(" | ".join(errors))