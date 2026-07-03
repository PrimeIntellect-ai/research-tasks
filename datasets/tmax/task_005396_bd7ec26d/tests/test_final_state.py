# test_final_state.py

import os
import shutil
import subprocess
import sqlite3
import pytest

def test_video_frames_extracted():
    frames_dir = "/home/user/video_frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist."
    frames = [f for f in os.listdir(frames_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    assert len(frames) > 0, "No frames were extracted to /home/user/video_frames/"

def test_go_binary_exists():
    binary_path = "/home/user/pipeline/filter"
    assert os.path.isfile(binary_path), f"Go binary missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Go binary at {binary_path} is not executable"

def test_model_json_exists():
    model_path = "/home/user/model.json"
    assert os.path.isfile(model_path), f"Model file missing at {model_path}"

def test_adversarial_corpus_filtering():
    binary_path = "/home/user/pipeline/filter"
    model_path = "/home/user/model.json"
    clean_corpus = "/test/eval_corpus/clean"
    evil_corpus = "/test/eval_corpus/evil"
    mixed_dir = "/test/eval_corpus/mixed"
    output_dir = "/test/eval_corpus/output"
    db_path = "/test/eval_corpus/test.db"

    # Setup directories
    os.makedirs(mixed_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Clean up mixed and output directories if they exist from previous runs
    for d in [mixed_dir, output_dir]:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
    if os.path.exists(db_path):
        os.remove(db_path)

    clean_files = []
    evil_files = []

    if os.path.exists(clean_corpus):
        for f in os.listdir(clean_corpus):
            if f.lower().endswith(('.jpg', '.jpeg')):
                clean_files.append(f)
                shutil.copy(os.path.join(clean_corpus, f), os.path.join(mixed_dir, f))

    if os.path.exists(evil_corpus):
        for f in os.listdir(evil_corpus):
            if f.lower().endswith(('.jpg', '.jpeg')):
                evil_files.append(f)
                shutil.copy(os.path.join(evil_corpus, f), os.path.join(mixed_dir, f))

    # Run the filter
    cmd = [
        binary_path,
        "--mode", "filter",
        "--input", mixed_dir,
        "--output", output_dir,
        "--model", model_path,
        "--db", db_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Filter binary failed with exit code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    output_files = set(os.listdir(output_dir))

    # Check that all clean files are preserved
    missing_clean = [f for f in clean_files if f not in output_files]
    assert len(missing_clean) == 0, f"{len(missing_clean)} of {len(clean_files)} clean modified/rejected: {missing_clean}"

    # Check that all evil files are rejected
    bypassed_evil = [f for f in evil_files if f in output_files]
    assert len(bypassed_evil) == 0, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {bypassed_evil}"

    # Check database
    assert os.path.isfile(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='features'")
    assert cursor.fetchone() is not None, "Table 'features' does not exist in the database."

    # Check rows count
    cursor.execute("SELECT COUNT(*) FROM features")
    count = cursor.fetchone()[0]
    assert count == len(clean_files), f"Expected {len(clean_files)} rows in the database, got {count}"

    conn.close()

def test_original_db_exists():
    db_path = "/home/user/features.db"
    assert os.path.isfile(db_path), f"Original database missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='features'")
    assert cursor.fetchone() is not None, "Table 'features' missing in /home/user/features.db"
    conn.close()

def test_clean_frames_exist():
    clean_dir = "/home/user/clean_frames"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist."
    frames = [f for f in os.listdir(clean_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    assert len(frames) > 0, "No filtered frames found in /home/user/clean_frames/"