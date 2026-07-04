# test_final_state.py

import os
import shutil
import tempfile
import subprocess
import pytest

def test_binary_exists():
    binary_path = "/home/user/motif_filter/target/release/motif_filter"
    assert os.path.exists(binary_path), f"Binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_adversarial_corpus():
    binary_path = "/home/user/motif_filter/target/release/motif_filter"
    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus path not found: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus path not found: {evil_dir}"

    with tempfile.TemporaryDirectory() as temp_input, tempfile.TemporaryDirectory() as temp_output:
        clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.fasta')]
        evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.fasta')]

        assert len(clean_files) > 0, "No clean files found."
        assert len(evil_files) > 0, "No evil files found."

        # Copy to a mixed input directory with prefixes to avoid any name collisions
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(temp_input, f"clean_{f}"))
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(temp_input, f"evil_{f}"))

        # Run the agent's binary
        result = subprocess.run([binary_path, temp_input, temp_output], capture_output=True, text=True)
        assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"

        output_files = set(os.listdir(temp_output))

        clean_missing = []
        for f in clean_files:
            if f"clean_{f}" not in output_files:
                clean_missing.append(f)

        evil_bypassed = []
        for f in evil_files:
            if f"evil_{f}" in output_files:
                evil_bypassed.append(f)

        errors = []
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_missing:
            errors.append(f"{len(clean_missing)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_missing)}")

        if errors:
            pytest.fail(" | ".join(errors))