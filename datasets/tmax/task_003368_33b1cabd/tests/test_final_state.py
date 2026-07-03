# test_final_state.py

import os
import subprocess
import pytest
import glob

DETECTOR_PATH = "/home/user/detector"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector binary not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary at {DETECTOR_PATH} is not executable"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_bypassed = []

    for c_file in clean_files:
        result = subprocess.run([DETECTOR_PATH, c_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(c_file))

    for e_file in evil_files:
        result = subprocess.run([DETECTOR_PATH, e_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(e_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_libcsv_compilation():
    so_path = "/app/libcsv-3.0.3/libcsv.so"
    a_path = "/app/libcsv-3.0.3/libcsv.a"
    # Depending on how it's built, it might be .so or .a, or inside .libs
    # We just check if the directory exists and make was run.
    assert os.path.isdir("/app/libcsv-3.0.3"), "libcsv directory missing"

    # Check if object files exist
    obj_files = glob.glob("/app/libcsv-3.0.3/*.o") + glob.glob("/app/libcsv-3.0.3/.libs/*.o")
    assert len(obj_files) > 0, "libcsv does not appear to have been compiled (no .o files found)."