# test_final_state.py

import os
import json
import time
import subprocess
import pytest
import csv
from pathlib import Path

def test_multi_service_integration():
    """
    Test that the Nginx -> FastAPI -> Redis -> Celery flow works.
    We upload a clean CSV via Nginx and wait for the Celery worker to write the stats file.
    """
    clean_csv_path = "/app/tests/corpora/clean/test_1.csv"
    stats_file = "/home/user/processed_stats.json"

    # Ensure clean CSV exists to test with
    if not os.path.exists(clean_csv_path):
        # Create a dummy clean CSV if it doesn't exist for the test
        os.makedirs(os.path.dirname(clean_csv_path), exist_ok=True)
        with open(clean_csv_path, "w") as f:
            f.write("id,locale,updated_at,translation\n1,en-US,2023-10-04T15:30:00Z,Hello\n")

    # Remove existing stats file if any
    if os.path.exists(stats_file):
        os.remove(stats_file)

    # Use curl to upload
    curl_cmd = [
        "curl", "-s", "-X", "POST",
        "-F", f"file=@{clean_csv_path}",
        "http://127.0.0.1:8080/upload"
    ]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"Upload failed with Nginx/FastAPI: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Upload request to Nginx timed out.")

    # Poll for the stats file for up to 5 seconds
    success = False
    for _ in range(10):
        if os.path.exists(stats_file):
            success = True
            break
        time.sleep(0.5)

    assert success, "Celery worker did not write to /home/user/processed_stats.json. Multi-service integration failed."

def test_translation_filter_clean_corpus(tmp_path):
    """
    Test the translation filter script against the clean corpus.
    Must preserve 100% of rows, normalize dates, and add lang_primary.
    """
    script_path = "/home/user/translation_filter.py"
    clean_dir = Path("/app/tests/corpora/clean")

    assert os.path.exists(script_path), f"Script not found at {script_path}"

    if not clean_dir.exists():
        pytest.skip("Clean corpus directory not found.")

    clean_files = list(clean_dir.glob("*.csv"))
    if not clean_files:
        pytest.skip("No clean CSV files found.")

    failed_files = []

    for csv_file in clean_files:
        out_file = tmp_path / f"out_{csv_file.name}"
        cmd = ["python3", script_path, str(csv_file), str(out_file)]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append((csv_file.name, "Script crashed or returned non-zero"))
            continue

        try:
            # The script must print a JSON summary to STDOUT
            # We extract the last valid JSON object from stdout
            lines = result.stdout.strip().split('\n')
            stats = None
            for line in reversed(lines):
                try:
                    stats = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

            if not stats:
                failed_files.append((csv_file.name, "No valid JSON output found in STDOUT"))
                continue

            if stats.get("invalid_rows_dropped", -1) != 0:
                failed_files.append((csv_file.name, f"Dropped {stats.get('invalid_rows_dropped')} rows, expected 0"))
                continue

            if not out_file.exists():
                failed_files.append((csv_file.name, "Output CSV not created"))
                continue

            # Check output CSV has lang_primary
            with open(out_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if "lang_primary" not in reader.fieldnames:
                    failed_files.append((csv_file.name, "Missing lang_primary column in output"))

        except Exception as e:
            failed_files.append((csv_file.name, str(e)))

    if failed_files:
        details = ", ".join([f"{f}: {reason}" for f, reason in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified or failed: {details}")

def test_translation_filter_evil_corpus(tmp_path):
    """
    Test the translation filter script against the evil corpus.
    Must drop malformed rows without crashing.
    """
    script_path = "/home/user/translation_filter.py"
    evil_dir = Path("/app/tests/corpora/evil")

    assert os.path.exists(script_path), f"Script not found at {script_path}"

    if not evil_dir.exists():
        pytest.skip("Evil corpus directory not found.")

    evil_files = list(evil_dir.glob("*.csv"))
    if not evil_files:
        pytest.skip("No evil CSV files found.")

    failed_files = []

    for csv_file in evil_files:
        out_file = tmp_path / f"out_{csv_file.name}"
        cmd = ["python3", script_path, str(csv_file), str(out_file)]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            failed_files.append((csv_file.name, "Script crashed on evil input"))
            continue

        try:
            lines = result.stdout.strip().split('\n')
            stats = None
            for line in reversed(lines):
                try:
                    stats = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

            if not stats:
                failed_files.append((csv_file.name, "No valid JSON output found in STDOUT"))
                continue

            if stats.get("invalid_rows_dropped", 0) == 0 and stats.get("total_input_rows", 0) > 0:
                # Assuming evil files have at least one invalid row
                failed_files.append((csv_file.name, "Failed to drop any invalid rows"))
                continue

        except Exception as e:
            failed_files.append((csv_file.name, str(e)))

    if failed_files:
        details = ", ".join([f"{f}: {reason}" for f, reason in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed or crashed: {details}")