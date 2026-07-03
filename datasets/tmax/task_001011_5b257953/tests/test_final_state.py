# test_final_state.py

import os
import subprocess
import pytest

def test_collect_diagnostics_success():
    """
    Test that Part 1 is completed: the vendored sh library is fixed
    and collect_diagnostics.py runs successfully without errors.
    """
    script_path = "/home/user/collect_diagnostics.py"
    assert os.path.isfile(script_path), f"Missing script {script_path}"

    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"collect_diagnostics.py failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\nStderr: {result.stderr}"
    )

    raw_logs_dir = "/home/user/raw_logs/"
    assert os.path.isdir(raw_logs_dir), f"Missing raw logs directory at {raw_logs_dir}"

    source_logs_dir = "/tmp/source_logs/"
    source_files = os.listdir(source_logs_dir)
    raw_files = os.listdir(raw_logs_dir)

    assert len(raw_files) > 0, "No files were copied to /home/user/raw_logs/"
    assert len(raw_files) == len(source_files), (
        f"Expected {len(source_files)} files in raw_logs, but found {len(raw_files)}."
    )

def test_sanitizer_clean_corpus():
    """
    Test that the sanitizer correctly accepts all clean logs (exit code 0).
    """
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Missing sanitizer script at {sanitizer_path}"

    clean_dir = "/app/data/corpora/clean/"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "Clean corpus directory is empty"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(["python3", sanitizer_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(
            f"{len(failed_files)} of {len(clean_files)} clean modified (rejected when they should be accepted). "
            f"Offending files: {', '.join(failed_files)}"
        )

def test_sanitizer_evil_corpus():
    """
    Test that the sanitizer correctly rejects all evil logs (exit code 1).
    """
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Missing sanitizer script at {sanitizer_path}"

    evil_dir = "/app/data/corpora/evil/"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "Evil corpus directory is empty"

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(["python3", sanitizer_path, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(
            f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted when they should be rejected). "
            f"Offending files: {', '.join(bypassed_files)}"
        )