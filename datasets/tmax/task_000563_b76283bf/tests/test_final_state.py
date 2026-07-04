# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_netlogger_compiled():
    """Verify that the netlogger binary is compiled and runs successfully."""
    binary_path = "/home/user/netlogger/netlogger"
    assert os.path.isfile(binary_path), f"netlogger binary not found at {binary_path}"

    try:
        result = subprocess.run([binary_path, "--version"], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"netlogger failed to execute properly. Return code: {result.returncode}, Stderr: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to run netlogger: {e}")

def test_log_sanitiser_clean_corpus():
    """Verify that the log sanitiser preserves all lines in the clean corpus."""
    sanitiser_path = "/home/user/log_sanitiser"
    assert os.path.isfile(sanitiser_path), f"log_sanitiser binary not found at {sanitiser_path}"

    clean_files = glob.glob("/app/corpus/clean/*.log")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    for file_path in clean_files:
        with open(file_path, 'r') as f:
            original_lines = f.read().splitlines()

        try:
            result = subprocess.run([sanitiser_path, file_path], capture_output=True, text=True, timeout=5)
            output_lines = result.stdout.splitlines()

            if original_lines != output_lines:
                failed_files.append(os.path.basename(file_path))
        except Exception as e:
            pytest.fail(f"Failed to run sanitiser on {file_path}: {e}")

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified: {', '.join(failed_files)}"

def test_log_sanitiser_evil_corpus():
    """Verify that the log sanitiser rejects all invalid lines in the evil corpus."""
    sanitiser_path = "/home/user/log_sanitiser"
    assert os.path.isfile(sanitiser_path), f"log_sanitiser binary not found at {sanitiser_path}"

    evil_files = glob.glob("/app/corpus/evil/*.log")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []

    for file_path in evil_files:
        try:
            result = subprocess.run([sanitiser_path, file_path], capture_output=True, text=True, timeout=5)
            output_lines = [line for line in result.stdout.splitlines() if line.strip()]

            if len(output_lines) > 0:
                failed_files.append(os.path.basename(file_path))
        except Exception as e:
            pytest.fail(f"Failed to run sanitiser on {file_path}: {e}")

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"