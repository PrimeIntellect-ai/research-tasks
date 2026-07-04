# test_final_state.py

import os
import subprocess
import pytest

def test_verification_log_exists():
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you complete the task?"
    with open(log_path, "r") as f:
        content = f.read()
    assert "SANITIZER BUILD COMPLETE" in content, f"Log file {log_path} does not contain the required text."

def test_libsqlparser_compiled():
    lib_path = "/app/sql-parser-c/libsqlparser.a"
    assert os.path.isfile(lib_path), f"Static library {lib_path} does not exist. Did you fix and compile the vendored package?"

    # Run make test in the vendored directory
    try:
        result = subprocess.run(["make", "test"], cwd="/app/sql-parser-c", capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"'make test' failed in /app/sql-parser-c. Output:\n{result.stdout}\n{result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to run 'make test' in /app/sql-parser-c: {e}")

def test_sanitizer_executable_exists():
    exe_path = "/home/user/query_sanitizer"
    assert os.path.isfile(exe_path), f"Sanitizer executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_adversarial_corpus_evil():
    exe_path = "/home/user/query_sanitizer"
    evil_dir = "/app/corpora/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed = []
    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        result = subprocess.run([exe_path, file_path], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil files bypassed rejection. Offending files: {', '.join(bypassed[:10])}{'...' if len(bypassed)>10 else ''}")

def test_adversarial_corpus_clean():
    exe_path = "/home/user/query_sanitizer"
    clean_dir = "/app/corpora/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    modified = []
    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        result = subprocess.run([exe_path, file_path], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean files were incorrectly rejected. Offending files: {', '.join(modified[:10])}{'...' if len(modified)>10 else ''}")