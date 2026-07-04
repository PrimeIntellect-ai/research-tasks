# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_uploads.sh"
EVIL_DIR = "/app/corpus/evil"
CLEAN_DIR = "/app/corpus/clean"

def run_script(payload: str) -> str:
    result = subprocess.run(
        ["bash", SCRIPT_PATH],
        input=payload,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_evil_corpus():
    assert os.path.exists(EVIL_DIR), f"Missing evil corpus directory at {EVIL_DIR}"

    files = sorted(os.listdir(EVIL_DIR))
    assert len(files) > 0, f"No files found in {EVIL_DIR}"

    bypassed = []
    for f in files:
        file_path = os.path.join(EVIL_DIR, f)
        with open(file_path, "r") as fp:
            payload = fp.read().strip()

        output = run_script(payload)
        if output != "REJECT":
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_clean_corpus():
    assert os.path.exists(CLEAN_DIR), f"Missing clean corpus directory at {CLEAN_DIR}"

    files = sorted(os.listdir(CLEAN_DIR))
    assert len(files) > 0, f"No files found in {CLEAN_DIR}"

    modified = []
    for f in files:
        file_path = os.path.join(CLEAN_DIR, f)
        with open(file_path, "r") as fp:
            payload = fp.read().strip()

        output = run_script(payload)
        if output != "ACCEPT":
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(files)} clean modified. Offending files: {', '.join(modified)}")