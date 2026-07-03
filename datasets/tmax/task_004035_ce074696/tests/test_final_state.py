# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"

def test_script_exists_and_executable():
    """Check if the detection script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable"

def run_script_on_file(file_path):
    """Run the detection script on a given file and return the output."""
    result = subprocess.run(
        [SCRIPT_PATH, file_path],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_adversarial_corpus():
    """
    Test the script against both the evil and clean corpora.
    Evil files must output 'MALICIOUS'.
    Clean files must output 'CLEAN'.
    """
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus dir missing: {EVIL_CORPUS_DIR}"
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus dir missing: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = [] # 'modified' contextually means incorrectly classified

    for ef in evil_files:
        output = run_script_on_file(ef)
        if output != "MALICIOUS":
            evil_bypassed.append((os.path.basename(ef), output))

    for cf in clean_files:
        output = run_script_on_file(cf)
        if output != "CLEAN":
            clean_modified.append((os.path.basename(cf), output))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: " + ", ".join([f"{f} (output: {o})" for f, o in evil_bypassed]))

    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (incorrectly classified). Offending files: " + ", ".join([f"{f} (output: {o})" for f, o in clean_modified]))

    if errors:
        pytest.fail("\n".join(errors))