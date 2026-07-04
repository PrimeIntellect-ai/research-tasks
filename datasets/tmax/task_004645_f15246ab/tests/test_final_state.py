# test_final_state.py

import os
import json
import subprocess
import pytest

EVIL_CORPUS = "/app/data/evil_logs.txt"
CLEAN_CORPUS = "/app/data/clean_logs.txt"
SANITIZER_BIN = "/home/user/sanitizer"
FINAL_STATS = "/home/user/final_stats.json"

def run_sanitizer(input_text: str) -> str:
    try:
        result = subprocess.run(
            [SANITIZER_BIN],
            input=input_text,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Sanitizer execution failed: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Sanitizer execution timed out.")

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_BIN), f"Sanitizer binary {SANITIZER_BIN} is missing."
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary {SANITIZER_BIN} is not executable."

def test_evil_corpus_sanitized():
    assert os.path.isfile(EVIL_CORPUS), f"Evil corpus {EVIL_CORPUS} is missing."

    with open(EVIL_CORPUS, "r") as f:
        evil_lines = f.read().strip().split('\n')

    bypassed_files = []

    for i, line in enumerate(evil_lines):
        if not line.strip():
            continue

        output = run_sanitizer(line + "\n").strip()

        try:
            out_json = json.loads(output)
        except json.JSONDecodeError:
            bypassed_files.append(f"Line {i+1}: Output is not valid JSON")
            continue

        # Check SSN
        if "ssn" in out_json:
            if out_json["ssn"] != "XXX-XX-XXXX":
                bypassed_files.append(f"Line {i+1}: SSN not masked properly")

        # Check Email
        if "email" in out_json:
            email_val = out_json["email"]
            if not email_val.startswith("***@"):
                bypassed_files.append(f"Line {i+1}: Email not masked properly")

        # Check Time Bucket
        if "time_bucket" not in out_json:
            bypassed_files.append(f"Line {i+1}: time_bucket missing")
        elif "timestamp" in out_json:
            expected_bucket = out_json["timestamp"][:16]
            if out_json["time_bucket"] != expected_bucket:
                bypassed_files.append(f"Line {i+1}: time_bucket incorrect")

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_lines)} evil bypassed: " + ", ".join(bypassed_files))

def test_clean_corpus_preserved():
    assert os.path.isfile(CLEAN_CORPUS), f"Clean corpus {CLEAN_CORPUS} is missing."

    with open(CLEAN_CORPUS, "r") as f:
        clean_lines = f.read().strip().split('\n')

    modified_files = []

    for i, line in enumerate(clean_lines):
        if not line.strip():
            continue

        orig_json = json.loads(line)
        output = run_sanitizer(line + "\n").strip()

        try:
            out_json = json.loads(output)
        except json.JSONDecodeError:
            modified_files.append(f"Line {i+1}: Output is not valid JSON")
            continue

        # Check preserved fields
        for k, v in orig_json.items():
            if k not in out_json or out_json[k] != v:
                modified_files.append(f"Line {i+1}: Field {k} modified or missing")

        # Check Time Bucket
        if "time_bucket" not in out_json:
            modified_files.append(f"Line {i+1}: time_bucket missing")
        elif "timestamp" in out_json:
            expected_bucket = out_json["timestamp"][:16]
            if out_json["time_bucket"] != expected_bucket:
                modified_files.append(f"Line {i+1}: time_bucket incorrect")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_lines)} clean modified: " + ", ".join(modified_files))

def test_final_stats_exists_and_valid():
    assert os.path.isfile(FINAL_STATS), f"Final stats file {FINAL_STATS} is missing. End-to-end pipeline may not have run."

    with open(FINAL_STATS, "r") as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{FINAL_STATS} does not contain valid JSON.")

    assert isinstance(stats, dict), f"Expected {FINAL_STATS} to contain a JSON object."
    assert len(stats) > 0, f"{FINAL_STATS} is empty. Pipeline did not process any logs."