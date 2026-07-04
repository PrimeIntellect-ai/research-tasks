# test_final_state.py
import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect_glitch.py"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.png"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.png"))

    assert len(evil_files) > 0, f"No files found in evil corpus {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No files found in clean corpus {CLEAN_CORPUS_DIR}"

    evil_bypassed = []
    clean_modified = []

    for img_path in evil_files:
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, img_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "GLITCH":
                evil_bypassed.append((os.path.basename(img_path), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(img_path), str(e)))

    for img_path in clean_files:
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, img_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append((os.path.basename(img_path), output))
        except Exception as e:
            clean_modified.append((os.path.basename(img_path), str(e)))

    error_messages = []
    if evil_bypassed:
        error_messages.append(
            f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. "
            f"Offending files: {', '.join(f[0] for f in evil_bypassed[:5])}"
            f"{'...' if len(evil_bypassed) > 5 else ''}"
        )
    if clean_modified:
        error_messages.append(
            f"{len(clean_modified)} of {len(clean_files)} clean modified (failed to identify as CLEAN). "
            f"Offending files: {', '.join(f[0] for f in clean_modified[:5])}"
            f"{'...' if len(clean_modified) > 5 else ''}"
        )

    assert not error_messages, " | ".join(error_messages)