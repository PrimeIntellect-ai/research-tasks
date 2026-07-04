# test_final_state.py

import os
import subprocess
import pytest

def test_filter_script_exists():
    script_path = "/home/user/filter.py"
    assert os.path.isfile(script_path), f"Missing filter script at {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/filter.py"
    clean_dir = "/app/data/clean"
    evil_dir = "/app/data/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_vendored_package_installed():
    # Verify the vendored package can be imported and works as expected
    try:
        import ts_distance
    except ImportError:
        pytest.fail("The vendored package 'ts_distance' is not installed or importable.")

    result = ts_distance.compute_dtw([1.0, 2.0], [1.0, 2.0])
    assert result == 0.0, "The compute_dtw function did not return the expected result."