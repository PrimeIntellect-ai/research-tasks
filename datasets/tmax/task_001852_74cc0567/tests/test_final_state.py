# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/expr_ffi"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
BINARY_PATH = os.path.join(PROJECT_DIR, "target/release/expr_ffi")
CI_SCRIPT_PATH = os.path.join(PROJECT_DIR, "ci_check.sh")

def test_cargo_build_release():
    """Verify that the project builds successfully in release mode."""
    result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Cargo build failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert os.path.isfile(BINARY_PATH), f"Binary not found at {BINARY_PATH} after successful build."

def test_adversarial_corpus_evil():
    """Verify that all files in the evil corpus are rejected (exit code 1)."""
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in the evil corpus."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")

def test_adversarial_corpus_clean():
    """Verify that all files in the clean corpus are accepted (exit code 0)."""
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in the clean corpus."

    modified_files = []
    for filepath in clean_files:
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified (failed to parse): {', '.join(modified_files)}")

def test_ci_script():
    """Verify that the CI check script exists and exits with 0."""
    assert os.path.isfile(CI_SCRIPT_PATH), f"CI script missing: {CI_SCRIPT_PATH}"

    result = subprocess.run(
        ["bash", CI_SCRIPT_PATH],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"CI script failed with exit code {result.returncode}:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"