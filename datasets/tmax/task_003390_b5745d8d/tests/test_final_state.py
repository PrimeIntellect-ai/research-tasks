# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_query_builder_installed():
    """Verify that the query-builder package is fixed and installed."""
    pyproject_path = "/app/vendored/query-builder-1.0.0/pyproject.toml"
    assert os.path.isfile(pyproject_path), f"File {pyproject_path} is missing"

    with open(pyproject_path, "r") as f:
        content = f.read()

    assert "fake-build-backend" not in content, "The deliberate error 'fake-build-backend' was not removed from pyproject.toml"

    try:
        import query_builder
    except ImportError:
        pytest.fail("The query_builder package is not installed or importable. Ensure you installed it after fixing pyproject.toml.")

def test_sanitizer_adversarial_corpus():
    """Verify the sanitizer correctly classifies clean and evil corpora."""
    sanitizer_script = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_script), f"Sanitizer script {sanitizer_script} is missing"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".json")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".json")]

    assert len(clean_files) > 0, "Clean corpus is empty"
    assert len(evil_files) > 0, "Evil corpus is empty"

    clean_failed = []
    for fpath in clean_files:
        result = subprocess.run([sys.executable, sanitizer_script, fpath], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "SAFE":
            clean_failed.append(os.path.basename(fpath))

    evil_failed = []
    for fpath in evil_files:
        result = subprocess.run([sys.executable, sanitizer_script, fpath], capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "UNSAFE":
            evil_failed.append(os.path.basename(fpath))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msgs:
        pytest.fail("Adversarial corpus verification failed:\n" + "\n".join(error_msgs))