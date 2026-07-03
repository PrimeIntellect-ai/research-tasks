# test_final_state.py

import os
import json
import tempfile
import subprocess
import pytest

EXECUTABLE = "/home/user/ingest"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus missing at {EVIL_CORPUS}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(EVIL_CORPUS, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run([EXECUTABLE, input_path, tmpdir], capture_output=True)

            # Should exit non-zero and not create the output file
            if result.returncode == 0 or os.path.exists(output_path):
                bypassed_files.append(filename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed validation: {', '.join(bypassed_files)}"

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus missing at {CLEAN_CORPUS}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(CLEAN_CORPUS, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run([EXECUTABLE, input_path, tmpdir], capture_output=True)

            # Should exit zero and create the output file
            if result.returncode != 0 or not os.path.exists(output_path):
                failed_files.append(filename)
                continue

            # Check if output is valid UTF-8 JSON
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected or modified: {', '.join(failed_files)}"