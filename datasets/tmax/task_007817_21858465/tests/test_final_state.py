# test_final_state.py

import os
import pytest

def hash_djb2(s):
    hash_val = 5381
    for c in s:
        hash_val = ((hash_val << 5) + hash_val) + ord(c)
        hash_val &= 0xFFFFFFFFFFFFFFFF  # emulate 64-bit unsigned long
    return hash_val

def test_deduped_configs_log():
    log_path = '/home/user/deduped_configs.log'
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    expected_entries = [
        "PORT=8080",
        "HOST_NAME=web-server-01",
        "DB_HOST=database.local",
        "DB_PORT=5432",
        "WORKER_THREADS=4",
        "QUEUE_URL=redis://localhost:6379",
        "HOST_NAME=cache-server-01"
    ]

    expected_lines = [f"[{hash_djb2(entry)}] {entry}" for entry in expected_entries]

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {log_path} do not match the expected output."

def test_pipeline_log():
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    expected_lines = [
        "DUPLICATE: DB_HOST=database.local",
        "DUPLICATE: DB_PORT=5432",
        "DUPLICATE: QUEUE_URL=redis://localhost:6379"
    ]

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {log_path} do not match the expected duplicates."

def test_c_source_code_regex():
    src_path = '/home/user/config_tracker.c'
    assert os.path.isfile(src_path), f"Source file {src_path} is missing."

    with open(src_path, 'r') as f:
        code = f.read()

    assert 'regcomp' in code, "The C program must use POSIX regex API 'regcomp'."
    assert 'regexec' in code, "The C program must use POSIX regex API 'regexec'."
    assert '<regex.h>' in code, "The C program must include <regex.h>."