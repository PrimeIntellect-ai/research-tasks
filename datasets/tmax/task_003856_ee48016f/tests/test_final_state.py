# test_final_state.py

import os
import subprocess
import pytest

def test_vendored_sql_builder_fixed():
    compiler_path = "/app/vendored_sql_builder/compiler.py"
    assert os.path.exists(compiler_path), f"Expected file {compiler_path} does not exist."

    with open(compiler_path, "r") as f:
        content = f.read()

    assert "if False" not in content, "The deliberate perturbation (hardcoded False) was not removed in compiler.py."
    assert "is_recursive" in content, "The fix using 'is_recursive' parameter is missing in compiler.py."

def test_query_sanitizer_exists():
    sanitizer_path = "/home/user/query_sanitizer.py"
    assert os.path.exists(sanitizer_path), f"Expected script {sanitizer_path} does not exist."
    assert os.path.isfile(sanitizer_path), f"Expected {sanitizer_path} to be a file."

def test_adversarial_corpus():
    sanitizer_path = "/home/user/query_sanitizer.py"
    assert os.path.exists(sanitizer_path), "Sanitizer script missing."

    clean_dir = "/home/user/corpora/clean/"
    evil_dir = "/home/user/corpora/evil/"

    assert os.path.exists(clean_dir), f"Clean corpus dir {clean_dir} missing."
    assert os.path.exists(evil_dir), f"Evil corpus dir {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["python3", sanitizer_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["python3", sanitizer_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))