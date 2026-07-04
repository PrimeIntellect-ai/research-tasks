# test_final_state.py

import os
import subprocess
import shutil
import pytest

CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"
PIPELINE_SCRIPT = "/home/user/pipeline.sh"
SANITIZER_EXEC = "/home/user/sanitizer"

def test_pipeline_script_exists():
    assert os.path.isfile(PIPELINE_SCRIPT), f"Pipeline script not found at {PIPELINE_SCRIPT}"
    assert os.access(PIPELINE_SCRIPT, os.X_OK) or os.path.exists(PIPELINE_SCRIPT), "Pipeline script should exist"

def test_sanitizer_executable_exists():
    assert os.path.isfile(SANITIZER_EXEC), f"Sanitizer executable not found at {SANITIZER_EXEC}"
    assert os.access(SANITIZER_EXEC, os.X_OK), f"Sanitizer at {SANITIZER_EXEC} is not executable"

def test_clean_corpus_preserved(tmp_path):
    output_dir = str(tmp_path / "clean_out")
    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run(["/bin/bash", PIPELINE_SCRIPT, CLEAN_CORPUS, output_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed on clean corpus:\n{result.stderr}"

    clean_files = []
    for root, _, files in os.walk(CLEAN_CORPUS):
        for f in files:
            if f.endswith(".log"):
                clean_files.append(os.path.relpath(os.path.join(root, f), CLEAN_CORPUS))

    assert len(clean_files) > 0, "No clean log files found to test."

    modified_clean = []
    missing_clean = []

    for rel_file in clean_files:
        in_path = os.path.join(CLEAN_CORPUS, rel_file)
        out_path = os.path.join(output_dir, rel_file)

        if not os.path.exists(out_path):
            missing_clean.append(rel_file)
            continue

        with open(in_path, "r") as f:
            in_content = f.read()
        with open(out_path, "r") as f:
            out_content = f.read()

        if in_content != out_content:
            modified_clean.append(rel_file)

    error_msgs = []
    if missing_clean:
        error_msgs.append(f"{len(missing_clean)} clean files missing in output: {missing_clean[:5]}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} clean files modified (not perfectly preserved): {modified_clean[:5]}")

    assert not error_msgs, " | ".join(error_msgs)

def test_evil_corpus_rejected(tmp_path):
    output_dir = str(tmp_path / "evil_out")
    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run(["/bin/bash", PIPELINE_SCRIPT, EVIL_CORPUS, output_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed on evil corpus:\n{result.stderr}"

    evil_files = []
    for root, _, files in os.walk(EVIL_CORPUS):
        for f in files:
            if f.endswith(".log"):
                evil_files.append(os.path.relpath(os.path.join(root, f), EVIL_CORPUS))

    assert len(evil_files) > 0, "No evil log files found to test."

    bypassed_evil = []

    for rel_file in evil_files:
        out_path = os.path.join(output_dir, rel_file)

        if os.path.exists(out_path):
            with open(out_path, "r") as f:
                content = f.read().strip()
            if content:
                bypassed_evil.append(rel_file)

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed sanitization (output not empty): {bypassed_evil[:5]}"