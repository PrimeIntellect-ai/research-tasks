# test_final_state.py
import os
import json
import tempfile
import subprocess
import pytest

EXECUTABLE = "/home/user/organizer"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"
PREFIX = "SECURE_ARCHIVE_"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_clean_corpus():
    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run([EXECUTABLE, CLEAN_CORPUS, out_dir], capture_output=True)

        clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.json')]
        processed_count = 0
        expected_files = []

        for cf in clean_files:
            with open(os.path.join(CLEAN_CORPUS, cf), 'r') as f:
                data = json.load(f)
                expected_files.append((PREFIX + data["filename"], data["content"]))

        out_files = os.listdir(out_dir)
        missing = []

        for expected_name, expected_content in expected_files:
            if expected_name not in out_files:
                missing.append(expected_name)
            else:
                with open(os.path.join(out_dir, expected_name), 'r') as f:
                    content = f.read()
                    assert content == expected_content, f"Content mismatch for {expected_name}"
                processed_count += 1

        assert not missing, f"{len(missing)} of {len(clean_files)} clean files modified/missing. Missing expected outputs: {missing}"
        assert processed_count == len(clean_files), f"Expected {len(clean_files)} clean files processed, got {processed_count}"

def test_evil_corpus():
    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run([EXECUTABLE, EVIL_CORPUS, out_dir], capture_output=True)

        evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.json')]
        out_files = [f for f in os.listdir(out_dir) if not f.startswith('.')]

        # If the program correctly rejects all evil files, it should not write any final files to the output directory.
        assert not out_files, f"{len(out_files)} of {len(evil_files)} evil bypassed. Files written to output directory: {out_files}"