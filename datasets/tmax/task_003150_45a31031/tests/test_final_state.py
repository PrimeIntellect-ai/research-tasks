# test_final_state.py

import os
import subprocess
import pytest
import sys

CLEAN_DIR = "/var/opt/corpora/clean"
EVIL_DIR = "/var/opt/corpora/evil"
SCRIPT_PATH = "/home/user/cleaner.py"

def test_unicodenorm_installed():
    try:
        import unicodenorm
        assert unicodenorm.is_malicious("\u202Eevil") is True, "unicodenorm.is_malicious did not return True for known malicious string."
    except ImportError:
        pytest.fail("unicodenorm package is not installed or cannot be imported.")
    except Exception as e:
        pytest.fail(f"unicodenorm.is_malicious failed: {e}")

def run_cleaner_on_file(filepath):
    with open(filepath, 'rb') as f:
        input_data = f.read()

    result = subprocess.run(
        [sys.executable, SCRIPT_PATH],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout, input_data

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    evil_bypassed = []
    clean_modified = []

    for ef in evil_files:
        filepath = os.path.join(EVIL_DIR, ef)
        output, _ = run_cleaner_on_file(filepath)
        # The evil corpus should be entirely rejected (empty output)
        if output != b"":
            evil_bypassed.append(ef)

    for cf in clean_files:
        filepath = os.path.join(CLEAN_DIR, cf)
        output, input_data = run_cleaner_on_file(filepath)
        # The clean corpus should be entirely preserved (output matches input exactly)
        if output != input_data:
            clean_modified.append(cf)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))