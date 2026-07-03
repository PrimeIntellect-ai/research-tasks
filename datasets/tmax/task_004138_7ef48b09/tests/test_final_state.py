# test_final_state.py
import os
import time
import requests
import pytest
import csv

def test_pipeline_adversarial_corpus():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"
    output_dir = "/home/user/output"

    assert os.path.exists(evil_dir), f"Evil corpus directory {evil_dir} not found."
    assert os.path.exists(clean_dir), f"Clean corpus directory {clean_dir} not found."
    assert os.path.exists(output_dir), f"Output directory {output_dir} not found."

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]

    # Send requests to the Flask API
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        try:
            resp = requests.post("http://127.0.0.1:5000/ingest", json={"filepath": filepath}, timeout=2)
            assert resp.status_code == 200, f"Failed to POST {filepath}, status {resp.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"API request failed for {filepath}. Is the Flask API running and correctly configured? Error: {e}")

    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        try:
            resp = requests.post("http://127.0.0.1:5000/ingest", json={"filepath": filepath}, timeout=2)
            assert resp.status_code == 200, f"Failed to POST {filepath}, status {resp.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"API request failed for {filepath}. Is the Flask API running and correctly configured? Error: {e}")

    # Wait for the Go worker to process the files
    expected_files = set(evil_files + clean_files)
    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        output_files = set(os.listdir(output_dir))
        if expected_files.issubset(output_files):
            break
        time.sleep(0.5)

    # Verify evil files are rejected (only header remains)
    evil_bypassed = []
    for f in evil_files:
        out_path = os.path.join(output_dir, f)
        if not os.path.exists(out_path):
            evil_bypassed.append(f"{f} (missing output)")
            continue
        with open(out_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)
            rows = list(reader)
            if len(rows) > 0:
                evil_bypassed.append(f)

    # Verify clean files are perfectly preserved
    clean_modified = []
    for f in clean_files:
        in_path = os.path.join(clean_dir, f)
        out_path = os.path.join(output_dir, f)
        if not os.path.exists(out_path):
            clean_modified.append(f"{f} (missing output)")
            continue

        with open(in_path, 'r') as fin, open(out_path, 'r') as fout:
            in_rows = list(csv.reader(fin))
            out_rows = list(csv.reader(fout))
            if in_rows != out_rows:
                clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))