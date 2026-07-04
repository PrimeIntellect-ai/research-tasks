# test_final_state.py

import os
import subprocess
import pytest

def test_tiny_graph_db_compiled():
    binary_path = "/app/tiny-graph-db/bin/tiny-graph-db"
    assert os.path.isfile(binary_path), f"The binary {binary_path} does not exist. Did you compile the package?"
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

    try:
        result = subprocess.run([binary_path, "--version"], capture_output=True, text=True, timeout=5)
        assert "tiny-graph-db version 1.2.0" in result.stdout or "tiny-graph-db version 1.2.0" in result.stderr, \
            f"Expected version output from {binary_path} --version, but got stdout: {result.stdout} stderr: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to run {binary_path}: {e}")

def test_query_sanitizer_script():
    script_path = "/home/user/query_sanitizer.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    evil_corpus = "/app/corpora/evil_queries.txt"
    clean_corpus = "/app/corpora/clean_queries.txt"

    assert os.path.isfile(evil_corpus), f"Evil corpus missing at {evil_corpus}"
    assert os.path.isfile(clean_corpus), f"Clean corpus missing at {clean_corpus}"

    with open(evil_corpus, 'r') as f:
        evil_queries = [line.strip() for line in f if line.strip()]

    with open(clean_corpus, 'r') as f:
        clean_queries = [line.strip() for line in f if line.strip()]

    evil_bypassed = []
    for query in evil_queries:
        result = subprocess.run([script_path, query], capture_output=True, text=True)
        # Should output REJECT and exit with 1
        if result.returncode != 1 or "REJECT" not in result.stdout.upper():
            evil_bypassed.append(query)

    clean_rejected = []
    for query in clean_queries:
        result = subprocess.run([script_path, query], capture_output=True, text=True)
        # Should output ACCEPT and exit with 0
        if result.returncode != 0 or "ACCEPT" not in result.stdout.upper():
            clean_rejected.append(query)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_queries)} evil queries bypassed: {evil_bypassed[:5]}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_queries)} clean queries rejected: {clean_rejected[:5]}")

    if errors:
        pytest.fail(" | ".join(errors))