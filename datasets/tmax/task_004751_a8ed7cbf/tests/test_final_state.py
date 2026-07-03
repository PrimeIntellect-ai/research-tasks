# test_final_state.py

import os
import time
import requests
import pytest
import csv
import math

def test_pipeline_and_worker():
    """
    Validates that the Nginx -> Flask -> Redis -> C++ Worker pipeline is fully functional,
    and that the worker correctly classifies the adversarial corpus.
    """
    # 1. Load reference stats
    ref_stats_path = '/home/user/data/reference_stats.csv'
    assert os.path.exists(ref_stats_path), f"Reference stats missing at {ref_stats_path}"

    ref_stats = {}
    with open(ref_stats_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == 'feature_id': 
                continue
            ref_stats[row[0]] = (float(row[1]), float(row[2]))

    # 2. Load corpora
    clean_corpus_path = '/home/user/tests/corpus/clean.csv'
    evil_corpus_path = '/home/user/tests/corpus/evil.csv'

    assert os.path.exists(clean_corpus_path), f"Clean corpus missing at {clean_corpus_path}"
    assert os.path.exists(evil_corpus_path), f"Evil corpus missing at {evil_corpus_path}"

    with open(clean_corpus_path, 'r') as f:
        clean_payloads = [line.strip() for line in f if line.strip()]

    with open(evil_corpus_path, 'r') as f:
        evil_payloads = [line.strip() for line in f if line.strip()]

    # 3. Inject payloads into the pipeline
    # We send both clean and evil payloads to the Nginx endpoint
    for payload in clean_payloads + evil_payloads:
        try:
            res = requests.post(
                'http://localhost:8080/api/ingest', 
                data=payload, 
                headers={'Content-Type': 'text/csv'}, 
                timeout=2
            )
            assert res.status_code == 200, f"Failed to ingest payload, status: {res.status_code}. Pipeline not configured correctly."
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to Nginx/Flask pipeline: {e}")

    # 4. Allow time for the C++ worker to process the queue
    time.sleep(3)

    # 5. Read outputs
    clean_output_path = '/home/user/worker/clean_output.csv'
    evil_output_path = '/home/user/worker/evil_output.csv'

    assert os.path.exists(clean_output_path), f"{clean_output_path} is missing. Worker did not create clean output."
    assert os.path.exists(evil_output_path), f"{evil_output_path} is missing. Worker did not create evil output."

    clean_out = {}
    with open(clean_output_path, 'r') as f:
        for row in csv.reader(f):
            if not row or row[0] == 'batch_id': 
                continue
            clean_out[row[0]] = float(row[2])

    evil_out = {}
    with open(evil_output_path, 'r') as f:
        for row in csv.reader(f):
            if not row or row[0] == 'batch_id': 
                continue
            evil_out[row[0]] = float(row[2])

    # 6. Verify evil payloads (must be rejected)
    evil_bypassed = []
    for payload in evil_payloads:
        parts = payload.split(',')
        batch_id = parts[0]
        feature_id = parts[1]
        vals = [float(x) for x in parts[2:]]

        # Recompute Z-score
        mean = sum(vals) / len(vals)
        ref_mean, ref_std = ref_stats[feature_id]
        # Standard error for sample mean: std / sqrt(n)
        # Wait, the prompt says: "one-sample Z-test against the reference mean and standard deviation"
        # Since standard deviation is given for the population, SE = std / sqrt(10)
        # However, if the user computed it as (mean - ref_mean) / ref_std, we'll check both or standard one.
        # "against the reference mean and standard deviation for that feature_id"
        # Let's compute the standard Z-score:
        z = (mean - ref_mean) / (ref_std / math.sqrt(len(vals)))

        if batch_id not in evil_out:
            evil_bypassed.append(batch_id)
        else:
            # Verify Z-score tolerance
            assert abs(abs(evil_out[batch_id]) - abs(z)) < 0.05 or abs(abs(evil_out[batch_id]) - abs((mean - ref_mean)/ref_std)) < 0.05, \
                f"Z-score mismatch for evil batch {batch_id}: expected {z:.3f}, got {evil_out[batch_id]}"

    # 7. Verify clean payloads (must be accepted)
    clean_modified = []
    for payload in clean_payloads:
        parts = payload.split(',')
        batch_id = parts[0]
        feature_id = parts[1]
        vals = [float(x) for x in parts[2:]]

        mean = sum(vals) / len(vals)
        ref_mean, ref_std = ref_stats[feature_id]
        z = (mean - ref_mean) / (ref_std / math.sqrt(len(vals)))

        if batch_id not in clean_out:
            clean_modified.append(batch_id)
        else:
            assert abs(abs(clean_out[batch_id]) - abs(z)) < 0.05 or abs(abs(clean_out[batch_id]) - abs((mean - ref_mean)/ref_std)) < 0.05, \
                f"Z-score mismatch for clean batch {batch_id}: expected {z:.3f}, got {clean_out[batch_id]}"

    # 8. Report failures
    if evil_bypassed or clean_modified:
        error_msg = f"{len(evil_bypassed)} of {len(evil_payloads)} evil bypassed. " \
                    f"{len(clean_modified)} of {len(clean_payloads)} clean modified.\n"
        if evil_bypassed:
            error_msg += f"Offending evil basenames (bypassed): {evil_bypassed[:10]}\n"
        if clean_modified:
            error_msg += f"Offending clean basenames (modified/missing): {clean_modified[:10]}"
        pytest.fail(error_msg)