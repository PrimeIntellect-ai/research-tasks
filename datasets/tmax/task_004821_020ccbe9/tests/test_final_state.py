# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import pytest

SCRIPT_PATH = "/home/user/process_sensors.py"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Agent script not found at {SCRIPT_PATH}"

def test_clean_corpus_processing():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus missing at {CLEAN_CORPUS}"

    with tempfile.TemporaryDirectory() as out_dir, tempfile.TemporaryDirectory() as rej_dir:
        cmd = [
            "python3", SCRIPT_PATH,
            "--input", CLEAN_CORPUS,
            "--output", out_dir,
            "--reject", rej_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on clean corpus. STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        expected_files = set(os.listdir(CLEAN_CORPUS))

        # Check output dir
        out_files = set(os.listdir(out_dir))
        # The script changes extension to .csv
        out_basenames = {os.path.splitext(f)[0] for f in out_files}
        expected_basenames = {os.path.splitext(f)[0] for f in expected_files}

        missing = expected_basenames - out_basenames

        assert not missing, f"{len(missing)} of {len(expected_files)} clean files were NOT accepted: {missing}"

        # Check reject dir
        rej_files = set(os.listdir(rej_dir))
        assert not rej_files, f"Clean files were incorrectly rejected: {rej_files}"

def test_evil_corpus_processing():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus missing at {EVIL_CORPUS}"

    with tempfile.TemporaryDirectory() as out_dir, tempfile.TemporaryDirectory() as rej_dir:
        cmd = [
            "python3", SCRIPT_PATH,
            "--input", EVIL_CORPUS,
            "--output", out_dir,
            "--reject", rej_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on evil corpus. STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        expected_files = set(os.listdir(EVIL_CORPUS))

        # Check reject dir
        rej_files = set(os.listdir(rej_dir))
        rej_basenames = {os.path.splitext(f)[0] for f in rej_files}
        expected_basenames = {os.path.splitext(f)[0] for f in expected_files}

        missing = expected_basenames - rej_basenames

        assert not missing, f"{len(missing)} of {len(expected_files)} evil files bypassed rejection: {missing}"

        # Check output dir
        out_files = set(os.listdir(out_dir))
        assert not out_files, f"Evil files were incorrectly accepted: {out_files}"