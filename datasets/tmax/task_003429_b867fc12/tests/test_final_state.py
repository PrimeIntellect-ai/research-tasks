# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/url_sanitizer.py"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_sanitizer_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No clean corpus files found"

    modified_files = []

    for filename in clean_files:
        input_path = os.path.join(CLEAN_DIR, filename)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            output_path = tmp.name

        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, input_path, output_path],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Script failed on {filename} with return code {result.returncode}:\n{result.stderr}"

            with open(input_path, 'r') as f:
                expected_lines = f.read().splitlines()
            with open(output_path, 'r') as f:
                actual_lines = f.read().splitlines()

            if expected_lines != actual_lines:
                modified_files.append(filename)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "No evil corpus files found"

    bypassed_files = []

    for filename in evil_files:
        input_path = os.path.join(EVIL_DIR, filename)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            output_path = tmp.name

        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, input_path, output_path],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Script failed on {filename} with return code {result.returncode}:\n{result.stderr}"

            with open(output_path, 'r') as f:
                actual_lines = f.read().splitlines()

            if len(actual_lines) > 0:
                bypassed_files.append(filename)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")