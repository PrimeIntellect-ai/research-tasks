# test_final_state.py

import os
import subprocess
import pytest

BIN_PATH = "/home/user/traffic_inspector"
LIB_PATH = "/app/picohttpparser/libpicohttpparser.so"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_shared_library_compiled():
    assert os.path.isfile(LIB_PATH), f"Shared library not found at {LIB_PATH}. Did you compile picohttpparser?"

def test_inspector_binary_compiled():
    assert os.path.isfile(BIN_PATH), f"Traffic inspector binary not found at {BIN_PATH}."
    assert os.access(BIN_PATH, os.X_OK), f"Traffic inspector binary at {BIN_PATH} is not executable."

def run_inspector(input_data: bytes) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    # Ensure the shared library can be found
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"/app/picohttpparser:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = "/app/picohttpparser"

    return subprocess.run(
        [BIN_PATH],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing at {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    bypassed = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, "rb") as f:
            input_data = f.read()

        result = run_inspector(input_data)

        if result.returncode != 1 or result.stdout != b"":
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil requests bypassed the inspector: {', '.join(bypassed)}")

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    modified_or_failed = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, "rb") as f:
            input_data = f.read()

        result = run_inspector(input_data)

        if result.returncode != 0:
            modified_or_failed.append(f"{filename} (exit code {result.returncode})")
            continue

        stdout_str = result.stdout.decode('utf-8', errors='ignore')

        # Check if Authorization header is redacted correctly if it was in the input
        input_str = input_data.decode('utf-8', errors='ignore')
        if "Authorization:" in input_str:
            if "Authorization: REDACTED" not in stdout_str:
                modified_or_failed.append(f"{filename} (Authorization header not REDACTED)")
                continue

    if modified_or_failed:
        pytest.fail(f"{len(modified_or_failed)} of {len(clean_files)} clean requests were incorrectly handled: {', '.join(modified_or_failed)}")