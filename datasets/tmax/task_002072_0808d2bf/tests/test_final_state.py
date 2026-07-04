# test_final_state.py

import os
import subprocess
import json
import tempfile
import pytest

EXECUTABLE = "/home/user/sanitiser"
CLEAN_CORPUS = "/app/clean/queries.jsonl"
EVIL_CORPUS = "/app/evil/queries.jsonl"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} not found."
    assert os.access(EXECUTABLE, os.X_OK), f"{EXECUTABLE} is not executable."

def run_sanitiser(input_file):
    result = subprocess.run([EXECUTABLE, input_file], capture_output=True, text=True)
    return set(result.stdout.strip().split())

def test_clean_corpus():
    assert os.path.isfile(CLEAN_CORPUS), f"Clean corpus missing at {CLEAN_CORPUS}"

    with open(CLEAN_CORPUS, 'r') as f:
        lines = f.read().splitlines()

    failed = []
    for line in lines:
        if not line.strip(): continue
        data = json.loads(line)
        query_id = data.get("id")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as tmp:
            tmp.write(line + '\n')
            tmp_path = tmp.name

        try:
            output_ids = run_sanitiser(tmp_path)
            if query_id not in output_ids:
                failed.append(query_id)
        finally:
            os.remove(tmp_path)

    assert not failed, f"{len(failed)} of {len(lines)} clean modified/rejected. Offending IDs: {failed}"

def test_evil_corpus():
    assert os.path.isfile(EVIL_CORPUS), f"Evil corpus missing at {EVIL_CORPUS}"

    with open(EVIL_CORPUS, 'r') as f:
        lines = f.read().splitlines()

    failed = []
    for line in lines:
        if not line.strip(): continue
        data = json.loads(line)
        query_id = data.get("id")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as tmp:
            tmp.write(line + '\n')
            tmp_path = tmp.name

        try:
            output_ids = run_sanitiser(tmp_path)
            if query_id in output_ids:
                failed.append(query_id)
        finally:
            os.remove(tmp_path)

    assert not failed, f"{len(failed)} of {len(lines)} evil bypassed. Offending IDs: {failed}"

def test_bulk_execution():
    # Test that running on the whole file at once works as expected
    clean_output = run_sanitiser(CLEAN_CORPUS)
    evil_output = run_sanitiser(EVIL_CORPUS)

    with open(CLEAN_CORPUS, 'r') as f:
        clean_ids = {json.loads(line)["id"] for line in f if line.strip()}

    with open(EVIL_CORPUS, 'r') as f:
        evil_ids = {json.loads(line)["id"] for line in f if line.strip()}

    missing_clean = clean_ids - clean_output
    bypassed_evil = evil_output.intersection(evil_ids)

    assert not missing_clean, f"Bulk run: missing clean IDs {missing_clean}"
    assert not bypassed_evil, f"Bulk run: bypassed evil IDs {bypassed_evil}"