# test_final_state.py

import os
import subprocess
import pytest

def test_validator_executable_exists():
    executable_path = "/home/user/src/validator"
    assert os.path.exists(executable_path), f"Executable not found at {executable_path}"
    assert os.path.isfile(executable_path), f"{executable_path} is not a file"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_validator_behavior_on_corpora():
    executable_path = "/home/user/src/validator"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus"
    assert len(evil_files) > 0, "No files found in evil corpus"

    clean_failures = []
    evil_failures = []

    # Check clean corpus
    for file_path in clean_files:
        try:
            result = subprocess.run(
                [executable_path, file_path],
                capture_output=True,
                text=True,
                timeout=2
            )
            output = result.stdout
            if output != "ACCEPT\n" or result.returncode != 0:
                clean_failures.append(os.path.basename(file_path))
        except subprocess.TimeoutExpired:
            clean_failures.append(f"{os.path.basename(file_path)} (timeout)")
        except Exception as e:
            clean_failures.append(f"{os.path.basename(file_path)} (error: {e})")

    # Check evil corpus
    for file_path in evil_files:
        try:
            result = subprocess.run(
                [executable_path, file_path],
                capture_output=True,
                text=True,
                timeout=2
            )
            output = result.stdout
            if output != "REJECT\n" or result.returncode != 0:
                evil_failures.append(os.path.basename(file_path))
        except subprocess.TimeoutExpired:
            evil_failures.append(f"{os.path.basename(file_path)} (timeout)")
        except Exception as e:
            evil_failures.append(f"{os.path.basename(file_path)} (error: {e})")

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))