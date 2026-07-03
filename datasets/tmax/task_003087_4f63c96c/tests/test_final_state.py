# test_final_state.py

import os
import subprocess
import pytest

def test_sanitizer_executable():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer executable not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer at {sanitizer_path} is not executable"

def test_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), "Sanitizer executable not found"

    evil_dir = "/app/evil/"
    clean_dir = "/app/clean/"

    evil_bypassed = []
    clean_modified = []

    evil_files = []
    if os.path.isdir(evil_dir):
        evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
        for ef in evil_files:
            file_path = os.path.join(evil_dir, ef)
            with open(file_path, "rb") as f:
                input_data = f.read()

            result = subprocess.run([sanitizer_path], input=input_data, capture_output=True)
            if result.stdout.strip():
                evil_bypassed.append(ef)

    clean_files = []
    if os.path.isdir(clean_dir):
        clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
        for cf in clean_files:
            file_path = os.path.join(clean_dir, cf)
            with open(file_path, "rb") as f:
                input_data = f.read()

            result = subprocess.run([sanitizer_path], input=input_data, capture_output=True)
            if result.stdout.strip() != input_data.strip():
                clean_modified.append(cf)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_final_target_nodes():
    csv_path = "/home/user/final_target_nodes.csv"
    assert os.path.isfile(csv_path), f"Missing final target nodes CSV at {csv_path}"

    with open(csv_path, "r", encoding="utf-8") as f:
        content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(content) == 3, f"Expected 3 lines in CSV (header + 2 rows), found {len(content)}"
    assert content[0] == "node_id,page_rank,cluster_id", f"Incorrect CSV header: {content[0]}"
    assert content[1] == "n1,0.5,C-8842", f"Expected row 1 to be 'n1,0.5,C-8842', got '{content[1]}'"
    assert content[2] == "n5,0.1,C-8842", f"Expected row 2 to be 'n5,0.1,C-8842', got '{content[2]}'"