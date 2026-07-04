# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_dataset_filter_binary():
    # Determine binary path
    binary_path = "/home/user/dataset_filter/target/debug/dataset_filter"
    if not os.path.exists(binary_path):
        binary_path = "/home/user/dataset_filter/target/release/dataset_filter"

    assert os.path.exists(binary_path), "Rust binary not found at /home/user/dataset_filter/target/debug/dataset_filter (or release)"

    schema_path = "/app/graph_schema.json"
    assert os.path.exists(schema_path), f"Schema file missing: {schema_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_corpus = glob.glob(os.path.join(clean_dir, "*"))
    evil_corpus = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_corpus) > 0, f"No files found in clean corpus directory: {clean_dir}"
    assert len(evil_corpus) > 0, f"No files found in evil corpus directory: {evil_dir}"

    clean_modified = []
    for clean_file in clean_corpus:
        res = subprocess.run([binary_path, schema_path, clean_file], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    evil_bypassed = []
    for evil_file in evil_corpus:
        res = subprocess.run([binary_path, schema_path, evil_file], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_corpus)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_corpus)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))