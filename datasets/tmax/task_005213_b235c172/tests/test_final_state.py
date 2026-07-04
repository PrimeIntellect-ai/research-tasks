# test_final_state.py

import os
import time
import json
import subprocess
import shutil
import pytest

LEGACY_PARSER = "/app/legacy_parser"
TEST_FILE = "/app/hidden_test_500MB.wal"
AGENT_BINARY = "/home/user/fast_organizer"
INCOMING_DIR = "/home/user/incoming"
ARCHIVE_DIR = "/home/user/dataset_backup/archive"
COMPILED_DATA = "/home/user/dataset_backup/compiled_data.json"

def get_json_records(filepath):
    records = []
    with open(filepath, 'r') as f:
        content = f.read().strip()
        if not content:
            return records

        # Try parsing as a single JSON array
        try:
            parsed = json.loads(content)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass

        # Try parsing as concatenated JSON objects or multiple arrays
        # A simple approach is to use a JSON decoder to parse sequentially
        decoder = json.JSONDecoder()
        idx = 0
        while idx < len(content):
            # skip whitespace
            while idx < len(content) and content[idx].isspace():
                idx += 1
            if idx >= len(content):
                break
            try:
                obj, end_idx = decoder.raw_decode(content, idx)
                if isinstance(obj, list):
                    records.extend(obj)
                else:
                    records.append(obj)
                idx = end_idx
            except json.JSONDecodeError:
                # If we can't parse further, just break and return what we have
                break
    return records

def test_fast_organizer_speed_and_accuracy():
    assert os.path.exists(AGENT_BINARY), f"Missing agent binary at {AGENT_BINARY}"
    assert os.access(AGENT_BINARY, os.X_OK), f"Agent binary {AGENT_BINARY} is not executable"

    # Time legacy parser
    t0 = time.time()
    legacy_proc = subprocess.run([LEGACY_PARSER, TEST_FILE], capture_output=True, text=True)
    legacy_time = time.time() - t0

    assert legacy_proc.returncode == 0, "Legacy parser failed to run on test file"
    legacy_records = json.loads(legacy_proc.stdout)

    # Prepare environment for agent binary
    for d in [INCOMING_DIR, ARCHIVE_DIR]:
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))

    if os.path.exists(COMPILED_DATA):
        os.remove(COMPILED_DATA)

    # Start agent binary
    agent_proc = subprocess.Popen([AGENT_BINARY])

    try:
        # Give it a moment to initialize inotify
        time.sleep(1)

        # Copy test file to incoming directory
        incoming_file = os.path.join(INCOMING_DIR, "test_speed.wal")
        archive_file = os.path.join(ARCHIVE_DIR, "test_speed.wal")

        t0 = time.time()
        shutil.copy2(TEST_FILE, incoming_file)

        # Wait for the file to be processed and moved to archive
        timeout = 60
        processed = False
        while time.time() - t0 < timeout:
            if os.path.exists(archive_file):
                processed = True
                break
            time.sleep(0.1)

        agent_time = time.time() - t0

        assert processed, f"Agent binary did not process the file within {timeout} seconds"

    finally:
        agent_proc.terminate()
        try:
            agent_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            agent_proc.kill()

    # Verify accuracy
    assert os.path.exists(COMPILED_DATA), f"Compiled data file missing at {COMPILED_DATA}"
    agent_records = get_json_records(COMPILED_DATA)

    assert len(agent_records) == len(legacy_records), f"Record count mismatch: expected {len(legacy_records)}, got {len(agent_records)}"

    # Compare a few records to ensure accuracy
    for i in range(len(legacy_records)):
        assert agent_records[i] == legacy_records[i], f"Record mismatch at index {i}: expected {legacy_records[i]}, got {agent_records[i]}"

    # Verify speedup
    speedup = legacy_time / agent_time
    assert speedup >= 10.0, f"Speedup too low: {speedup:.2f}x (Legacy: {legacy_time:.2f}s, Agent: {agent_time:.2f}s). Expected >= 10.0x"