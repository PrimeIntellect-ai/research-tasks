# test_final_state.py

import os
import base64
import socket
import pytest

WORKSPACE = "/home/user/workspace"
CLEAN_DIR = os.path.join(WORKSPACE, "corpus", "clean")
EVIL_DIR = os.path.join(WORKSPACE, "corpus", "evil")
OUT_DIR = os.path.join(WORKSPACE, "out_clean")

def get_redis_counter(key: str) -> int:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 6379))
        s.sendall(f"GET {key}\r\n".encode('utf-8'))
        resp = s.recv(1024).decode('utf-8')
        s.close()

        lines = resp.split('\r\n')
        if len(lines) >= 2 and lines[0].startswith('$') and lines[0] != '$-1':
            return int(lines[1])
        return 0
    except Exception:
        return 0

def test_out_clean_directory_exists():
    assert os.path.isdir(OUT_DIR), f"Output directory {OUT_DIR} does not exist. The agent failed to create it or run the sanitizer."

def test_clean_corpus_processed():
    if not os.path.isdir(CLEAN_DIR):
        pytest.fail(f"Clean corpus directory {CLEAN_DIR} is missing.")
    if not os.path.isdir(OUT_DIR):
        pytest.fail(f"Output directory {OUT_DIR} is missing.")

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    total_clean = len(clean_files)

    missing_or_modified = []

    for filename in clean_files:
        in_path = os.path.join(CLEAN_DIR, filename)
        out_path = os.path.join(OUT_DIR, filename)

        if not os.path.isfile(out_path):
            missing_or_modified.append(filename)
            continue

        with open(in_path, 'r') as f:
            b64_data = f.read().strip()

        expected_decoded = base64.b64decode(b64_data)

        with open(out_path, 'rb') as f:
            actual_decoded = f.read()

        if actual_decoded != expected_decoded:
            missing_or_modified.append(filename)

    if missing_or_modified:
        pytest.fail(f"{len(missing_or_modified)} of {total_clean} clean modified/missing. Offending files: {', '.join(missing_or_modified)}")

def test_evil_corpus_rejected():
    if not os.path.isdir(EVIL_DIR):
        pytest.fail(f"Evil corpus directory {EVIL_DIR} is missing.")
    if not os.path.isdir(OUT_DIR):
        pytest.fail(f"Output directory {OUT_DIR} is missing.")

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    total_evil = len(evil_files)

    bypassed = []

    for filename in evil_files:
        out_path = os.path.join(OUT_DIR, filename)
        if os.path.isfile(out_path):
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {total_evil} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_redis_counter():
    if not os.path.isdir(CLEAN_DIR) or not os.path.isdir(EVIL_DIR):
        pytest.fail("Corpus directories are missing, cannot compute total files.")

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    total_expected = len(clean_files) + len(evil_files)

    actual_count = get_redis_counter("processed_files")

    assert actual_count == total_expected, f"Redis 'processed_files' counter is {actual_count}, expected {total_expected}."