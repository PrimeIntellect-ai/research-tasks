# test_final_state.py

import os
import subprocess
import hashlib
import pytest

VALIDATE_SCRIPT = "/home/user/validate_doc_tree.sh"
EVIL_CORPUS = "/home/user/corpora/evil"
CLEAN_CORPUS = "/home/user/corpora/clean"
PARSER_SCRIPT = "/app/vendored/doc_compiler_v2.1/bin/parser.sh"
MANIFEST_FILE = "/home/user/safe_docs_manifest.txt"
SYNC_LOG = "/home/user/sync_requests.log"

def test_validate_doc_tree_exists():
    assert os.path.isfile(VALIDATE_SCRIPT), f"Missing script: {VALIDATE_SCRIPT}"
    assert os.access(VALIDATE_SCRIPT, os.X_OK), f"Script not executable: {VALIDATE_SCRIPT}"

def test_adversarial_corpus_validate_script():
    evil_dirs = sorted([os.path.join(EVIL_CORPUS, d) for d in os.listdir(EVIL_CORPUS) if os.path.isdir(os.path.join(EVIL_CORPUS, d))])
    clean_dirs = sorted([os.path.join(CLEAN_CORPUS, d) for d in os.listdir(CLEAN_CORPUS) if os.path.isdir(os.path.join(CLEAN_CORPUS, d))])

    evil_bypassed = []
    for edir in evil_dirs:
        try:
            result = subprocess.run([VALIDATE_SCRIPT, edir], capture_output=True, timeout=5)
            if result.returncode != 1:
                evil_bypassed.append(os.path.basename(edir))
        except subprocess.TimeoutExpired:
            evil_bypassed.append(f"{os.path.basename(edir)} (timeout)")

    clean_modified = []
    for cdir in clean_dirs:
        try:
            result = subprocess.run([VALIDATE_SCRIPT, cdir], capture_output=True, timeout=5)
            if result.returncode != 0:
                clean_modified.append(os.path.basename(cdir))
        except subprocess.TimeoutExpired:
            clean_modified.append(f"{os.path.basename(cdir)} (timeout)")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_dirs)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_dirs)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_vendored_doc_compiler_fixed():
    assert os.path.isfile(PARSER_SCRIPT), f"Missing parser script: {PARSER_SCRIPT}"

    # Test it doesn't hang on evil corpus
    evil_dirs = [os.path.join(EVIL_CORPUS, d) for d in os.listdir(EVIL_CORPUS) if os.path.isdir(os.path.join(EVIL_CORPUS, d))]
    if evil_dirs:
        test_dir = evil_dirs[0]
        try:
            result = subprocess.run(["bash", PARSER_SCRIPT, test_dir], capture_output=True, timeout=5)
        except subprocess.TimeoutExpired:
            pytest.fail("Vendored doc compiler still hangs on infinite symlink loops.")

def test_manifest_generation():
    assert os.path.isfile(MANIFEST_FILE), f"Missing manifest file: {MANIFEST_FILE}"

    # Parse sync_requests.log
    clean_requested_dirs = []
    if os.path.isfile(SYNC_LOG):
        with open(SYNC_LOG, "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.startswith("PATH:"):
                    path = line.split("PATH:", 1)[1].strip()
                    if path.startswith(CLEAN_CORPUS):
                        clean_requested_dirs.append(path)

    expected_hashes = []
    for cdir in clean_requested_dirs:
        for root, dirs, files in os.walk(cdir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    # compute sha256
                    hasher = hashlib.sha256()
                    with open(filepath, "rb") as f:
                        hasher.update(f.read())
                    expected_hashes.append(f"{hasher.hexdigest()}  {filepath}")

    expected_hashes.sort()

    with open(MANIFEST_FILE, "r") as f:
        actual_hashes = f.read().splitlines()

    assert actual_hashes == expected_hashes, "Manifest file content does not match expected sorted SHA256 checksums of clean requested .md files."