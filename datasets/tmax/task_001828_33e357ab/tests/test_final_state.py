# test_final_state.py

import os
import subprocess
import shutil
import pytest

EVIL_CORPUS_PATH = "/app/data/corpus/evil/"
CLEAN_CORPUS_PATH = "/app/data/corpus/clean/"
SCRIPT_PATH = "/home/user/clean_dataset.sh"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_bayes_filter_compiled():
    binary_path = "/app/bayes_text_filter-1.2.0/bayes_filter"
    assert os.path.isfile(binary_path), f"Binary {binary_path} was not compiled. Did you fix the Makefile and run make?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_clean_corpus_preserved(tmp_path):
    out_dir = tmp_path / "out_clean"
    out_dir.mkdir()

    # Run the user's script on the clean corpus
    result = subprocess.run(
        [SCRIPT_PATH, CLEAN_CORPUS_PATH, str(out_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed on clean corpus with error: {result.stderr}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_PATH) if f.endswith('.txt')]
    missing_files = []
    modified_files = []

    for fname in clean_files:
        src = os.path.join(CLEAN_CORPUS_PATH, fname)
        dst = os.path.join(out_dir, fname)
        if not os.path.isfile(dst):
            missing_files.append(fname)
        else:
            with open(src, 'r') as f_src, open(dst, 'r') as f_dst:
                if f_src.read() != f_dst.read():
                    modified_files.append(fname)

    total_clean = len(clean_files)
    failed_clean = len(missing_files) + len(modified_files)

    error_msg = f"{failed_clean} of {total_clean} clean modified/rejected."
    if missing_files:
        error_msg += f"\nMissing files: {missing_files[:5]}"
    if modified_files:
        error_msg += f"\nModified files: {modified_files[:5]}"

    assert failed_clean == 0, error_msg

def test_evil_corpus_rejected(tmp_path):
    out_dir = tmp_path / "out_evil"
    out_dir.mkdir()

    # Run the user's script on the evil corpus
    result = subprocess.run(
        [SCRIPT_PATH, EVIL_CORPUS_PATH, str(out_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed on evil corpus with error: {result.stderr}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_PATH) if f.endswith('.txt')]
    bypassed_files = []

    for fname in evil_files:
        dst = os.path.join(out_dir, fname)
        if os.path.isfile(dst):
            bypassed_files.append(fname)

    total_evil = len(evil_files)
    failed_evil = len(bypassed_files)

    error_msg = f"{failed_evil} of {total_evil} evil bypassed."
    if bypassed_files:
        error_msg += f"\nOffending files: {bypassed_files[:5]}"

    assert failed_evil == 0, error_msg