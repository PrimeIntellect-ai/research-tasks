# test_final_state.py
import os
import sys
import json
import csv
import time
import urllib.request
import pytest
import importlib.util

CLEAN_CORPUS = "/app/tests/corpus_clean.jsonl"
EVIL_CORPUS = "/app/tests/corpus_evil.jsonl"
CSV_FILE = "/home/user/processed_logs.csv"
SANITIZER_PATH = "/home/user/sanitizer.py"

def load_sanitizer():
    assert os.path.exists(SANITIZER_PATH), f"{SANITIZER_PATH} does not exist."
    spec = importlib.util.spec_from_file_location("sanitizer", SANITIZER_PATH)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    spec.loader.exec_module(sanitizer)
    assert hasattr(sanitizer, "process_and_sanitize"), "process_and_sanitize function missing."
    return sanitizer.process_and_sanitize

def test_sanitizer_logic():
    process_and_sanitize = load_sanitizer()

    clean_failed = []
    if os.path.exists(CLEAN_CORPUS):
        with open(CLEAN_CORPUS, "rb") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line: continue
                result = process_and_sanitize(line)
                if result is None:
                    clean_failed.append(f"Line {i+1}")
                else:
                    # check masking
                    assert result.get("ssn") == "XXX-XX-XXXX", f"SSN not masked properly in clean line {i+1}"
                    email = result.get("email", "")
                    assert email.startswith("hidden@"), f"Email not masked properly in clean line {i+1}"

    evil_failed = []
    if os.path.exists(EVIL_CORPUS):
        with open(EVIL_CORPUS, "rb") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line: continue
                try:
                    result = process_and_sanitize(line)
                except Exception:
                    result = None
                if result is not None:
                    evil_failed.append(f"Line {i+1}")

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} clean records rejected: {', '.join(clean_failed[:5])}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} evil records bypassed: {', '.join(evil_failed[:5])}")

    assert not errors, "Sanitizer logic failed:\n" + "\n".join(errors)

def test_end_to_end_worker():
    # POST data to API
    clean_lines = []
    if os.path.exists(CLEAN_CORPUS):
        with open(CLEAN_CORPUS, "rb") as f:
            clean_lines = [line.strip() for line in f if line.strip()]

    evil_lines = []
    if os.path.exists(EVIL_CORPUS):
        with open(EVIL_CORPUS, "rb") as f:
            evil_lines = [line.strip() for line in f if line.strip()]

    for line in clean_lines + evil_lines:
        req = urllib.request.Request("http://127.0.0.1:8080/ingest", data=line, method="POST")
        try:
            urllib.request.urlopen(req, timeout=2)
        except Exception as e:
            pytest.fail(f"Failed to POST to ingestion API: {e}")

    # Wait for worker to process
    time.sleep(5)

    assert os.path.exists(CSV_FILE), f"CSV file {CSV_FILE} was not created by the worker."

    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ["user_id", "email", "ssn", "age", "event_type"], "CSV headers are incorrect."

    # Check that only clean lines are present, and correctly masked
    assert len(rows) >= len(clean_lines), f"Expected at least {len(clean_lines)} rows in CSV, found {len(rows)}."

    for row in rows:
        assert row["ssn"] == "XXX-XX-XXXX", f"Row found with unmasked SSN: {row}"
        assert row["email"].startswith("hidden@"), f"Row found with unmasked email: {row}"

    # Since we don't know exact user_ids, we just ensure no evil lines slipped through
    # by checking the count. We expect exactly the number of clean lines (assuming empty CSV before).
    # If the worker processed previous runs, there might be more, but all must be clean.
    # The sanitizer logic test already ensures evil lines return None.