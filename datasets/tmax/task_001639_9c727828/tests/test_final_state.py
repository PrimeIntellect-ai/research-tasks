# test_final_state.py
import os
import subprocess
import pytest

DETECTOR_BIN = "/home/user/detector"
EVIL_CORPUS = "/app/corpus/evil/"
CLEAN_CORPUS = "/app/corpus/clean/"

def test_detector_exists_and_executable():
    assert os.path.isfile(DETECTOR_BIN), f"Detector binary not found at {DETECTOR_BIN}"
    assert os.access(DETECTOR_BIN, os.X_OK), f"Detector binary at {DETECTOR_BIN} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus missing: {EVIL_CORPUS}"
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus missing: {CLEAN_CORPUS}"

    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = [] # 'modified' in terms of classification, i.e., false positives

    for filepath in evil_files:
        try:
            result = subprocess.run([DETECTOR_BIN, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "MALICIOUS":
                evil_bypassed.append((os.path.basename(filepath), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(filepath), str(e)))

    for filepath in clean_files:
        try:
            result = subprocess.run([DETECTOR_BIN, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append((os.path.basename(filepath), output))
        except Exception as e:
            clean_modified.append((os.path.basename(filepath), str(e)))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed:")
        for f, out in evil_bypassed:
            error_messages.append(f"  - {f} (output: {out!r})")

    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (false positive):")
        for f, out in clean_modified:
            error_messages.append(f"  - {f} (output: {out!r})")

    if error_messages:
        pytest.fail("\n".join(error_messages))