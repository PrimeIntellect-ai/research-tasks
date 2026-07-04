# test_final_state.py
import os
import subprocess
import pytest

EVIL_DIR = "/app/corpus/evil"
CLEAN_DIR = "/app/corpus/clean"
SCANNER_PATH = "/home/user/scanner.go"

def run_scanner(filepath):
    try:
        result = subprocess.run(
            ["go", "run", SCANNER_PATH, filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_scanner_exists():
    assert os.path.isfile(SCANNER_PATH), f"Scanner Go program is missing at {SCANNER_PATH}"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing at {EVIL_DIR}"
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing at {CLEAN_DIR}"

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, f"Evil corpus directory {EVIL_DIR} is empty"
    assert len(clean_files) > 0, f"Clean corpus directory {CLEAN_DIR} is empty"

    evil_bypassed = []
    for f in evil_files:
        output = run_scanner(f)
        if output != "EVIL":
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        output = run_scanner(f)
        if output != "CLEAN":
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail("\n".join(errors))