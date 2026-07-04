# test_final_state.py

import os
import csv
import subprocess
import pytest
from io import StringIO

FALLBACKS_CSV = "/home/user/fallbacks.csv"
SANITIZER_BIN = "/home/user/loc_sanitizer"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_fallbacks_extracted():
    """Verify that fallbacks.csv was extracted and formatted correctly."""
    assert os.path.isfile(FALLBACKS_CSV), f"Missing {FALLBACKS_CSV}"
    with open(FALLBACKS_CSV, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_pairs = {
        ("es-AR", "es-ES"),
        ("fr-CA", "fr-FR"),
        ("pt-BR", "pt-PT"),
        ("zh-HK", "zh-TW")
    }

    actual_pairs = set()
    for line in content.splitlines():
        parts = line.split(",")
        if len(parts) == 2:
            actual_pairs.add((parts[0].strip(), parts[1].strip()))

    missing = expected_pairs - actual_pairs
    assert not missing, f"Missing fallback pairs in {FALLBACKS_CSV}: {missing}"

def test_sanitizer_executable():
    """Verify that the loc_sanitizer binary exists and is executable."""
    assert os.path.isfile(SANITIZER_BIN), f"Missing {SANITIZER_BIN}"
    assert os.access(SANITIZER_BIN, os.X_OK), f"{SANITIZER_BIN} is not executable"

def compute_expected_clean(input_text, fallbacks):
    """Compute the expected output for a clean CSV file."""
    reader = csv.reader(StringIO(input_text))
    output = StringIO()
    writer = csv.writer(output, lineterminator='\n')

    for row in reader:
        if len(row) >= 3:
            msg_id, loc, trans = row[0], row[1], row[2]
            if not trans and loc in fallbacks:
                row[2] = "[FALLBACK_APPLIED]"
        writer.writerow(row)

    return output.getvalue()

def test_corpus_processing():
    """Verify sanitizer behavior on clean and evil corpora."""
    assert os.path.isfile(SANITIZER_BIN), "Sanitizer binary not found."

    fallbacks = {}
    if os.path.isfile(FALLBACKS_CSV):
        with open(FALLBACKS_CSV, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    fallbacks[parts[0]] = parts[1]

    # Process Clean Corpus
    clean_failed = []
    if os.path.isdir(CLEAN_CORPUS):
        for fname in os.listdir(CLEAN_CORPUS):
            if not fname.endswith(".csv"):
                continue
            fpath = os.path.join(CLEAN_CORPUS, fname)
            with open(fpath, "rb") as f:
                input_bytes = f.read()

            # Run sanitizer
            proc = subprocess.run([SANITIZER_BIN, FALLBACKS_CSV], input=input_bytes, capture_output=True)
            actual_output = proc.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n")

            input_text = input_bytes.decode("utf-8")
            expected_output = compute_expected_clean(input_text, fallbacks).replace("\r\n", "\n")

            if actual_output.strip() != expected_output.strip():
                clean_failed.append(fname)

    # Process Evil Corpus
    evil_failed = []
    if os.path.isdir(EVIL_CORPUS):
        for fname in os.listdir(EVIL_CORPUS):
            if not fname.endswith(".csv"):
                continue
            fpath = os.path.join(EVIL_CORPUS, fname)
            with open(fpath, "rb") as f:
                input_bytes = f.read()

            proc = subprocess.run([SANITIZER_BIN, FALLBACKS_CSV], input=input_bytes, capture_output=True)
            actual_output_bytes = proc.stdout

            # All emitted rows must be valid UTF-8
            try:
                actual_output_bytes.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                evil_failed.append(fname)
                continue

            # Check if any invalid utf-8 row slipped through
            # Since we don't have a strict parser in test, we just ensure the output is valid utf-8
            # and doesn't contain the known bad strings if they were decoded.
            pass

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} clean files modified or incorrectly processed: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} evil files bypassed validation (emitted invalid UTF-8): {', '.join(evil_failed)}")

    assert not errors, " | ".join(errors)