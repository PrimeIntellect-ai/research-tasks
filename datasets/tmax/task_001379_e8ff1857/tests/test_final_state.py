# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/redirect_detector.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_sso_decrypt_binary_exists():
    binary_path = "/app/vendored-sso-auth-1.2.0/sso-decrypt"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you run 'make'?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/redirect_detector.sh"
    evil_corpus = "/app/corpus/evil"
    clean_corpus = "/app/corpus/clean"

    # Test Evil Corpus
    try:
        evil_output = subprocess.check_output([script_path, evil_corpus], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed when running on evil corpus. Output:\n{e.output}")

    evil_files = [f for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    evil_bypassed = []

    for filename in evil_files:
        expected_line = f"{filename}: EVIL"
        if expected_line not in evil_output:
            evil_bypassed.append(filename)

    # Test Clean Corpus
    try:
        clean_output = subprocess.check_output([script_path, clean_corpus], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed when running on clean corpus. Output:\n{e.output}")

    clean_files = [f for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]
    clean_modified = []

    for filename in clean_files:
        expected_line = f"{filename}: CLEAN"
        if expected_line not in clean_output:
            clean_modified.append(filename)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (flagged incorrectly): {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))