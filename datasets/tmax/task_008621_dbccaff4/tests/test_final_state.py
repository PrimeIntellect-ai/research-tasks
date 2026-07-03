# test_final_state.py

import os
import re
import subprocess
import pytest

def test_bad_payload_recovered():
    payload_path = "/home/user/metrics-daemon/bad_payload.txt"
    assert os.path.exists(payload_path), f"File {payload_path} was not recovered."

    with open(payload_path, "r") as f:
        content = f.read()

    expected_content = "METRIC:CPU_USAGE INVALID_CHARS\n"
    assert content == expected_content, f"Content of {payload_path} is incorrect. Expected {repr(expected_content)}, got {repr(content)}."

def test_leak_commit_identified():
    leak_file_path = "/home/user/leak_commit.txt"
    expected_file_path = "/tmp/expected_leak_commit.txt"

    assert os.path.exists(leak_file_path), f"File {leak_file_path} does not exist."
    assert os.path.exists(expected_file_path), f"Truth file {expected_file_path} is missing."

    with open(leak_file_path, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_file_path, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Incorrect leak commit hash. Expected {expected_hash}, got {actual_hash}."

def test_parser_fixed():
    parser_path = "/home/user/metrics-daemon/parser.c"
    assert os.path.exists(parser_path), f"File {parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    # Look for the strstr block and ensure there's a free(buf) before return NULL
    # A simple regex to check if free(buf) is present inside the if (strstr(...)) block
    pattern = r'if\s*\(\s*strstr\s*\(\s*buf\s*,\s*"INVALID_CHARS"\s*\)\s*\)\s*\{[^}]*free\s*\(\s*buf\s*\)\s*;[^}]*return\s+NULL\s*;[^}]*\}'
    match = re.search(pattern, content)
    assert match is not None, "Memory leak in parser.c is not fixed. Expected `free(buf);` before `return NULL;` inside the `strstr` block."

def test_queue_fixed():
    queue_path = "/home/user/metrics-daemon/queue.c"
    assert os.path.exists(queue_path), f"File {queue_path} is missing."

    with open(queue_path, "r") as f:
        content = f.read()

    # Check if enqueue function has mutex locks
    enqueue_pattern = r'void\s+enqueue\s*\([^)]*\)\s*\{([^}]+)\}'
    match = re.search(enqueue_pattern, content)
    assert match is not None, "Could not find enqueue function in queue.c."

    enqueue_body = match.group(1)

    assert "pthread_mutex_lock" in enqueue_body, "Missing pthread_mutex_lock in enqueue function."
    assert "pthread_mutex_unlock" in enqueue_body, "Missing pthread_mutex_unlock in enqueue function."

def test_compiles_cleanly():
    repo_path = "/home/user/metrics-daemon"
    try:
        # Run make clean first to ensure a fresh build
        subprocess.run(["make", "clean"], cwd=repo_path, check=True, capture_output=True)
        # Run make
        result = subprocess.run(["make"], cwd=repo_path, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Compilation failed. Make output:\n{e.stderr}"

    binary_path = os.path.join(repo_path, "metrics-daemon")
    assert os.path.exists(binary_path), f"Binary {binary_path} was not created after make."