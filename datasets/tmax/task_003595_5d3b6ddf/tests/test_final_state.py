# test_final_state.py
import os
import subprocess
import tempfile
import pytest

EVIL_CORPUS_PATH = "/app/corpora/evil/"
CLEAN_CORPUS_PATH = "/app/corpora/clean/"
SANITIZER_SCRIPT = "/home/user/sanitizer.py"

def test_sanitizer_script_exists():
    assert os.path.isfile(SANITIZER_SCRIPT), f"Missing sanitizer script at {SANITIZER_SCRIPT}"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_PATH) if os.path.isfile(os.path.join(EVIL_CORPUS_PATH, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(EVIL_CORPUS_PATH, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                ["python3", SANITIZER_SCRIPT, input_path, output_path],
                capture_output=True
            )

            if result.returncode != 1 or os.path.exists(output_path):
                bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_PATH) if os.path.isfile(os.path.join(CLEAN_CORPUS_PATH, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(CLEAN_CORPUS_PATH, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                ["python3", SANITIZER_SCRIPT, input_path, output_path],
                capture_output=True
            )

            if result.returncode != 0 or not os.path.exists(output_path):
                modified.append(filename)
                continue

            with open(input_path, "rb") as f_in, open(output_path, "rb") as f_out:
                if f_in.read() != f_out.read():
                    modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified. Offending files: {', '.join(modified)}")