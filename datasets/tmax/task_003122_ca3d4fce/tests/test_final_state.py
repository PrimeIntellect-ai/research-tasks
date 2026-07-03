# test_final_state.py

import os
import subprocess
import sqlite3
import csv
import pytest

VALIDATE_SCRIPT = "/home/user/validate_schema.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
EXTRACTED_FRAMES = "/home/user/extracted_frames.csv"
TELEMETRY_DB = "/home/user/telemetry.db"
MAX_FRAMES_CSV = "/home/user/max_frames_per_sec.csv"


def test_validate_schema_adversarial_corpus():
    """
    Test the validate_schema.py script against the clean and evil corpora.
    Clean files must exit with 0, evil files must exit with 1.
    """
    assert os.path.isfile(VALIDATE_SCRIPT), f"Validation script not found: {VALIDATE_SCRIPT}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_bypassed = []

    for clean_file in clean_files:
        result = subprocess.run(["python3", VALIDATE_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        result = subprocess.run(["python3", VALIDATE_SCRIPT, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean failed: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))


def test_extracted_frames():
    """
    Test that the extracted_frames.csv file was created and contains valid telemetry.
    """
    assert os.path.isfile(EXTRACTED_FRAMES), f"Extracted frames file not found: {EXTRACTED_FRAMES}"

    with open(EXTRACTED_FRAMES, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Extracted frames file is empty."

    for row in rows:
        assert len(row) == 2, f"Expected 2 columns, got {len(row)} in row: {row}"
        try:
            timestamp = float(row[0])
            size = int(row[1])
            assert timestamp >= 0, f"Timestamp must be non-negative: {timestamp}"
            assert size > 0, f"Size must be strictly greater than 0: {size}"
        except ValueError as e:
            pytest.fail(f"Invalid data type in extracted frames: {row} - {e}")


def test_telemetry_db():
    """
    Test that the telemetry.db database was created, contains the frames table,
    and has an index.
    """
    assert os.path.isfile(TELEMETRY_DB), f"Database not found: {TELEMETRY_DB}"

    conn = sqlite3.connect(TELEMETRY_DB)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='frames';")
    assert cursor.fetchone() is not None, "Table 'frames' not found in database."

    # Check index existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='frames';")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No index found on the 'frames' table."

    conn.close()


def test_max_frames_per_sec():
    """
    Test that the max_frames_per_sec.csv file was created and has the correct format.
    """
    assert os.path.isfile(MAX_FRAMES_CSV), f"Result CSV not found: {MAX_FRAMES_CSV}"

    with open(MAX_FRAMES_CSV, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['window_start', 'max_size'], f"Incorrect headers: {headers}"

        rows = list(reader)
        assert len(rows) > 0, "Result CSV is empty (excluding headers)."

        for row in rows:
            assert len(row) == 2, f"Expected 2 columns, got {len(row)} in row: {row}"
            try:
                window_start = float(row[0])
                max_size = int(row[1])
                assert window_start >= 0, f"Window start must be non-negative: {window_start}"
                assert max_size > 0, f"Max size must be strictly greater than 0: {max_size}"
            except ValueError as e:
                pytest.fail(f"Invalid data type in result CSV: {row} - {e}")