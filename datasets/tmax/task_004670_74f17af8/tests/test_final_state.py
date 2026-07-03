# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect_corruption.py"
JSON_PATH = "/home/user/corrupted_frames.json"
CLEAN_CORPUS_DIR = "/verifier/eval_corpus/clean/"
EVIL_CORPUS_DIR = "/verifier/eval_corpus/evil/"
EXPECTED_CORRUPTED_FRAMES = [14, 15, 16, 55, 92, 110, 111, 148]

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_json_output_exists_and_correct():
    assert os.path.isfile(JSON_PATH), f"JSON output file {JSON_PATH} does not exist."

    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    assert isinstance(data, list), f"JSON output must be a list, got {type(data)}."
    assert data == EXPECTED_CORRUPTED_FRAMES, (
        f"Corrupted frames list incorrect. Expected {EXPECTED_CORRUPTED_FRAMES}, got {data}."
    )

def test_adversarial_corpus_evil():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_CORPUS_DIR} not found.")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.png')]
    assert len(evil_files) > 0, f"No PNG files found in {EVIL_CORPUS_DIR}."

    bypassed = []
    for img_path in evil_files:
        result = subprocess.run(["python3", SCRIPT_PATH, img_path], capture_output=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(img_path))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}")

def test_adversarial_corpus_clean():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_CORPUS_DIR} not found.")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.png')]
    assert len(clean_files) > 0, f"No PNG files found in {CLEAN_CORPUS_DIR}."

    modified = []
    for img_path in clean_files:
        result = subprocess.run(["python3", SCRIPT_PATH, img_path], capture_output=True)
        if result.returncode != 0:
            modified.append(os.path.basename(img_path))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (rejected): {modified}")