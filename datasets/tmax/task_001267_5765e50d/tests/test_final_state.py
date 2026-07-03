# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_run_filter_sh_exists_and_executable():
    script_path = "/home/user/run_filter.sh"
    assert os.path.isfile(script_path), f"Wrapper script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Wrapper script {script_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/run_filter.sh"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test evil corpus
        for filename in evil_files:
            input_file = os.path.join(evil_dir, filename)
            output_file = os.path.join(tmpdir, f"out_{filename}")

            result = subprocess.run([script_path, input_file, output_file], capture_output=True, text=True)
            if result.returncode != 0:
                evil_bypassed.append(f"{filename} (script failed with code {result.returncode})")
                continue

            if not os.path.exists(output_file):
                continue

            with open(output_file, "r") as f:
                content = f.read().strip()
                if content:
                    evil_bypassed.append(filename)

        # Test clean corpus
        for filename in clean_files:
            input_file = os.path.join(clean_dir, filename)
            output_file = os.path.join(tmpdir, f"out_{filename}")

            result = subprocess.run([script_path, input_file, output_file], capture_output=True, text=True)
            if result.returncode != 0:
                clean_modified.append(f"{filename} (script failed with code {result.returncode})")
                continue

            if not os.path.exists(output_file):
                clean_modified.append(f"{filename} (output file missing)")
                continue

            with open(input_file, "r") as f_in, open(output_file, "r") as f_out:
                in_lines = f_in.readlines()
                out_lines = f_out.readlines()
                if in_lines != out_lines:
                    clean_modified.append(filename)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))