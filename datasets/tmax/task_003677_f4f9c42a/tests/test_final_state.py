# test_final_state.py

import os
import json
import subprocess
import tempfile
import shutil
import pytest

def test_package_installed_and_fixed():
    """Verify that the ml_artifact_tracker package is installed and the core module is fixed."""
    try:
        from tracker.core import Tracker
        Tracker()
    except ImportError as e:
        pytest.fail(f"Failed to import Tracker. The package might not be installed or the import error is not fixed: {e}")
    except Exception as e:
        pytest.fail(f"Tracker instantiated with an error: {e}")

def test_script_exists():
    """Check if the user script exists."""
    script_path = "/home/user/detect_corrupted.py"
    assert os.path.isfile(script_path), f"Script {script_path} not found."

def test_evil_corpus_rejected():
    """Iterate over every file in the evil corpus and assert the script rejects it."""
    script_path = "/home/user/detect_corrupted.py"
    evil_dir = "/app/corpora/evil"

    if not os.path.isdir(evil_dir):
        pytest.skip(f"Evil corpus directory {evil_dir} not found.")

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        os.makedirs(input_dir, exist_ok=True)
        output_file = os.path.join(tmpdir, "out.txt")

        for fname in evil_files:
            file_path = os.path.join(evil_dir, fname)
            dest_path = os.path.join(input_dir, fname)
            shutil.copy(file_path, dest_path)

            if os.path.exists(output_file):
                os.remove(output_file)

            subprocess.run(
                ["python", script_path, "--input-dir", input_dir, "--output", output_file],
                capture_output=True,
                text=True
            )

            if os.path.exists(output_file):
                with open(output_file, "r") as f:
                    content = f.read().strip()
                if content:
                    bypassed.append(fname)

            os.remove(dest_path)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_clean_corpus_preserved():
    """Iterate over every file in the clean corpus and assert the script accepts it."""
    script_path = "/home/user/detect_corrupted.py"
    clean_dir = "/app/corpora/clean"

    if not os.path.isdir(clean_dir):
        pytest.skip(f"Clean corpus directory {clean_dir} not found.")

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        os.makedirs(input_dir, exist_ok=True)
        output_file = os.path.join(tmpdir, "out.txt")

        for fname in clean_files:
            file_path = os.path.join(clean_dir, fname)
            dest_path = os.path.join(input_dir, fname)
            shutil.copy(file_path, dest_path)

            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                expected_id = str(data.get("artifact_id", ""))
            except Exception:
                expected_id = ""

            if os.path.exists(output_file):
                os.remove(output_file)

            subprocess.run(
                ["python", script_path, "--input-dir", input_dir, "--output", output_file],
                capture_output=True,
                text=True
            )

            passed = False
            if os.path.exists(output_file):
                with open(output_file, "r") as f:
                    content = f.read().strip()
                if expected_id and expected_id in content:
                    passed = True

            if not passed:
                modified.append(fname)

            os.remove(dest_path)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (rejected): {', '.join(modified)}")