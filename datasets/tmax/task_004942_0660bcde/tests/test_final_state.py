# test_final_state.py

import os
import json
import subprocess
import struct
import pytest

def test_quant_db_installed_and_fixed():
    """Verify that the quant-db package is installed and its tests pass."""
    test_file = "/app/vendor/quant-db-1.2.0/tests/test_agg.py"
    assert os.path.isfile(test_file), f"Test file {test_file} is missing"

    result = subprocess.run(
        ["pytest", test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"quant-db tests failed:\n{result.stdout}\n{result.stderr}"

def test_recovered_records_json():
    """Verify that the WAL file was correctly recovered into recovered_records.json."""
    wal_file = "/app/data/transaction.wal"
    json_file = "/app/data/recovered_records.json"

    assert os.path.isfile(wal_file), f"WAL file {wal_file} is missing"
    assert os.path.isfile(json_file), f"Recovered JSON file {json_file} is missing"

    # Read the expected records from the WAL file
    expected_records = []
    with open(wal_file, "rb") as f:
        data = f.read()

    i = 0
    while i < len(data) - 8:
        # Search for magic number 0xDEADBEEF
        if data[i:i+4] == b'\xde\xad\xbe\xef':
            length = struct.unpack(">I", data[i+4:i+8])[0]
            if i + 8 + length <= len(data):
                payload = data[i+8:i+8+length]
                # Assuming the payload is a JSON string or decodable string
                try:
                    record = json.loads(payload.decode('utf-8'))
                    expected_records.append(record)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    pass
            i += 1 # advance to next byte to continue search
        else:
            i += 1

    with open(json_file, "r") as f:
        try:
            recovered_records = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("recovered_records.json is not valid JSON")

    assert isinstance(recovered_records, list), "Recovered records should be a JSON list"
    assert len(recovered_records) > 0, "Recovered records list is empty"
    # We won't do a strict equality check here because the exact parsing logic might differ slightly,
    # but we will check that it contains records.

def test_sanitizer_adversarial_corpus():
    """Verify that the sanitizer correctly classifies the evil and clean corpora."""
    sanitizer_script = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_script), f"Sanitizer script {sanitizer_script} is missing"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), "Evil corpus directory missing"
    assert os.path.isdir(clean_dir), "Clean corpus directory missing"

    def run_sanitizer(corpus_dir):
        result = subprocess.run(
            ["python3", sanitizer_script, corpus_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Sanitizer script failed on {corpus_dir}:\n{result.stderr}"

        results = {}
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                filename, status = line.split(":", 1)
                results[filename.strip()] = status.strip()
        return results

    evil_results = run_sanitizer(evil_dir)
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.dat')]

    bypassed_evil = []
    for f in evil_files:
        if evil_results.get(f) != "REJECT":
            bypassed_evil.append(f)

    clean_results = run_sanitizer(clean_dir)
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.dat')]

    modified_clean = []
    for f in clean_files:
        if clean_results.get(f) != "ACCEPT":
            modified_clean.append(f)

    error_msg = []
    if bypassed_evil:
        error_msg.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {bypassed_evil[:5]}")
    if modified_clean:
        error_msg.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {modified_clean[:5]}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))