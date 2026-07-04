# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/config_filter.py"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"
APPROVED_DIR = "/home/user/approved_configs"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus missing at {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus missing at {EVIL_CORPUS}"

    if not os.path.isdir(APPROVED_DIR):
        os.makedirs(APPROVED_DIR, exist_ok=True)

    evil_files = sorted([f for f in os.listdir(EVIL_CORPUS) if f.endswith('.lzc')])
    clean_files = sorted([f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.lzc')])

    evil_bypassed = []
    clean_failed = []

    # Test Evil Corpus
    for ef in evil_files:
        ef_path = os.path.join(EVIL_CORPUS, ef)
        yaml_path = os.path.join(APPROVED_DIR, ef.replace('.lzc', '.yaml'))

        # Ensure clean state before run
        if os.path.exists(yaml_path):
            os.remove(yaml_path)

        result = subprocess.run(["python3", SCRIPT_PATH, ef_path], capture_output=True)

        # Evil files must be rejected (exit code != 0) and must not produce a yaml file
        if result.returncode == 0 or os.path.exists(yaml_path):
            evil_bypassed.append(ef)

    # Test Clean Corpus
    for cf in clean_files:
        cf_path = os.path.join(CLEAN_CORPUS, cf)
        yaml_path = os.path.join(APPROVED_DIR, cf.replace('.lzc', '.yaml'))

        # Ensure clean state before run
        if os.path.exists(yaml_path):
            os.remove(yaml_path)

        result = subprocess.run(["python3", SCRIPT_PATH, cf_path], capture_output=True)

        # Clean files must be accepted (exit code == 0) and must produce a yaml file
        if result.returncode != 0 or not os.path.exists(yaml_path):
            clean_failed.append(cf)

    err_msgs = []
    if evil_bypassed:
        err_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        err_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))