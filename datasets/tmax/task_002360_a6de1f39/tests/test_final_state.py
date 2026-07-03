# test_final_state.py

import os
import subprocess
import pytest

def test_vendored_library_built():
    """Verify that the vendored library was successfully compiled."""
    lib_path = "/app/vendored/libstatscsv-1.0/libstatscsv.a"
    assert os.path.isfile(lib_path), f"Vendored library {lib_path} was not built. Did you fix the compilation errors and run make?"

def test_detector_executable_exists():
    """Verify that the detector executable exists and is executable."""
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable {detector_path} is missing."
    assert os.access(detector_path, os.X_OK), f"Detector {detector_path} is not executable."

def test_adversarial_corpus():
    """Verify that the detector correctly classifies all clean and evil datasets."""
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isfile(detector_path), f"Detector executable {detector_path} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}."

    clean_modified = []
    evil_bypassed = []

    # Check clean corpus: exit code MUST be 0
    for cf in clean_files:
        result = subprocess.run([detector_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    # Check evil corpus: exit code MUST NOT be 0
    for ef in evil_files:
        result = subprocess.run([detector_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))