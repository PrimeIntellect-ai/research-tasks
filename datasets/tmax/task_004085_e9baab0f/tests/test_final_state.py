# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/sanitize_fasta.sh"
CLEAN_DIR = "/home/user/data/clean"
EVIL_DIR = "/home/user/data/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path is not a file: {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script is not executable: {SCRIPT_PATH}"

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_DIR}"

    modified_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(CLEAN_DIR, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run([SCRIPT_PATH, input_path, output_path], capture_output=True, text=True)
            if result.returncode != 0:
                modified_files.append((filename, f"Script failed with return code {result.returncode}"))
                continue

            if not os.path.exists(output_path):
                modified_files.append((filename, "Output file not created"))
                continue

            with open(input_path, 'r') as f_in, open(output_path, 'r') as f_out:
                input_content = f_in.read()
                output_content = f_out.read()

            if input_content != output_content:
                modified_files.append((filename, "Output does not match input exactly"))

    if modified_files:
        error_msg = f"{len(modified_files)} of {len(clean_files)} clean files modified or failed.\n"
        error_msg += "Offending files:\n" + "\n".join([f"{name}: {reason}" for name, reason in modified_files[:10]])
        if len(modified_files) > 10:
            error_msg += f"\n... and {len(modified_files) - 10} more."
        pytest.fail(error_msg)

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_DIR}"

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(EVIL_DIR, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run([SCRIPT_PATH, input_path, output_path], capture_output=True, text=True)
            if result.returncode != 0:
                # If it failed, it didn't bypass, but it's not ideal. We'll accept failure as rejection.
                continue

            if os.path.exists(output_path):
                with open(output_path, 'r') as f_out:
                    output_content = f_out.read().strip()
                if output_content:
                    bypassed_files.append(filename)

    if bypassed_files:
        error_msg = f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed sanitization.\n"
        error_msg += "Offending files:\n" + "\n".join(bypassed_files[:10])
        if len(bypassed_files) > 10:
            error_msg += f"\n... and {len(bypassed_files) - 10} more."
        pytest.fail(error_msg)