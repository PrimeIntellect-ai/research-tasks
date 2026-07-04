# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_inotifywait_installed():
    """Test that inotifywait was successfully built and installed."""
    binary_path = "/home/user/local/bin/inotifywait"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

    result = subprocess.run([binary_path, "--help"], capture_output=True, text=True)
    assert result.returncode == 0, f"inotifywait --help failed with exit code {result.returncode}"

def test_sanitize_manifest_exists():
    """Test that the sanitize_manifest.sh script exists and is executable."""
    script_path = "/home/user/sanitize_manifest.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_clean_corpus():
    """Test that the script accepts all clean corpus files and outputs valid UTF-8."""
    script_path = "/home/user/sanitize_manifest.sh"
    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    if not clean_files:
        pytest.skip("No clean corpus files found.")

    failed_files = []
    for f in clean_files:
        if not os.path.isfile(f):
            continue

        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f"{os.path.basename(f)} (exit code {result.returncode})")
            continue

        try:
            stdout_str = result.stdout.decode('utf-8')
            if not stdout_str.strip():
                failed_files.append(f"{os.path.basename(f)} (empty stdout)")
        except UnicodeDecodeError:
            failed_files.append(f"{os.path.basename(f)} (invalid UTF-8 output)")

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_evil_corpus():
    """Test that the script rejects all evil corpus files and prints nothing to stdout."""
    script_path = "/home/user/sanitize_manifest.sh"
    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    if not evil_files:
        pytest.skip("No evil corpus files found.")

    failed_files = []
    for f in evil_files:
        if not os.path.isfile(f):
            continue

        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode == 0:
            failed_files.append(f"{os.path.basename(f)} (exit code 0)")
        elif result.stdout != b'':
            failed_files.append(f"{os.path.basename(f)} (stdout not empty)")

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"