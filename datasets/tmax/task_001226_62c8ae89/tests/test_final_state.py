# test_final_state.py

import os
import subprocess
import pytest

def test_libb64_compilation():
    """Test that the vendored libb64 package has been successfully compiled."""
    # We check if the base64 executable was built, which implies make succeeded.
    # Alternatively, we can just run make and ensure it exits 0.
    # The prompt says "Running `make` in `/app/libb64-1.2` successfully builds `base64/base64`"

    # Let's run make in the directory to ensure it compiles without errors
    result = subprocess.run(
        ["make"], 
        cwd="/app/libb64-1.2", 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"Compilation of libb64 failed. Make output:\n{result.stderr}\n{result.stdout}"

    # Check if the expected output file exists
    executable_path = "/app/libb64-1.2/base64/base64"
    assert os.path.exists(executable_path), f"Expected compiled executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable"


def test_sanitizer_exists():
    """Test that the sanitizer program is compiled and exists."""
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.exists(sanitizer_path), f"Sanitizer executable not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer at {sanitizer_path} is not executable"


def test_sanitizer_clean_corpus():
    """Test that the sanitizer accepts all clean files (exit code 0)."""
    clean_dir = "/app/corpus/clean/"
    sanitizer_path = "/home/user/sanitizer"

    assert os.path.exists(sanitizer_path), "Sanitizer not found."

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run([sanitizer_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")


def test_sanitizer_evil_corpus():
    """Test that the sanitizer rejects all evil files (exit code 1)."""
    evil_dir = "/app/corpus/evil/"
    sanitizer_path = "/home/user/sanitizer"

    assert os.path.exists(sanitizer_path), "Sanitizer not found."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run([sanitizer_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")