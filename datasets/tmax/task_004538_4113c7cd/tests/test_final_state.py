# test_final_state.py

import os
import subprocess
import pytest
import ast

EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"
SANITIZER_SCRIPT = "/home/user/sanitizer.py"
REQUESTER_SCRIPT = "/home/user/requester.py"

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_SCRIPT), f"Sanitizer script missing at {SANITIZER_SCRIPT}"

def test_requester_exists():
    assert os.path.isfile(REQUESTER_SCRIPT), f"Requester script missing at {REQUESTER_SCRIPT}"

def test_requester_uses_asyncio():
    with open(REQUESTER_SCRIPT, 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    uses_asyncio = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'asyncio':
                    uses_asyncio = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == 'asyncio':
                uses_asyncio = True

    assert uses_asyncio, "The requester.py script must use asyncio to replicate the concurrency pattern."

def test_sanitizer_evil_corpus():
    if not os.path.isfile(SANITIZER_SCRIPT):
        pytest.fail(f"Cannot test evil corpus: {SANITIZER_SCRIPT} does not exist.")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    assert evil_files, f"No JSON files found in {EVIL_DIR}"

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", SANITIZER_SCRIPT, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 1:
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_sanitizer_clean_corpus():
    if not os.path.isfile(SANITIZER_SCRIPT):
        pytest.fail(f"Cannot test clean corpus: {SANITIZER_SCRIPT} does not exist.")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    assert clean_files, f"No JSON files found in {CLEAN_DIR}"

    modified = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", SANITIZER_SCRIPT, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            modified.append(os.path.basename(filepath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/rejected: {', '.join(modified)}")