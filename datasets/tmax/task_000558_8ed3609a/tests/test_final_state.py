# test_final_state.py

import os
import glob
import subprocess
import pytest

DETECTOR_PATH = "/home/user/detector"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_PATH), f"Detector binary not found at {DETECTOR_PATH}"
    assert os.access(DETECTOR_PATH, os.X_OK), f"Detector binary at {DETECTOR_PATH} is not executable"

def test_detector_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.wav"))
    assert len(clean_files) > 0, f"No clean WAV files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for wav_file in clean_files:
        result = subprocess.run([DETECTOR_PATH, wav_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(wav_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_files)}")

def test_detector_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.wav"))
    assert len(evil_files) > 0, f"No evil WAV files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for wav_file in evil_files:
        result = subprocess.run([DETECTOR_PATH, wav_file], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(wav_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}")