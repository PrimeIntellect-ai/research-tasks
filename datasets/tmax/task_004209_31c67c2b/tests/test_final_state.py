# test_final_state.py

import os
import json
import numpy as np
from scipy.stats import wasserstein_distance

WORKSPACE = '/home/user/workspace/pipeline'
RESULTS_FILE = os.path.join(WORKSPACE, 'results.json')
SEQUENCES_FILE = os.path.join(WORKSPACE, 'sequences.json')
REF_DIST_FILE = os.path.join(WORKSPACE, 'reference_dist.npy')

def compute_expected_wasserstein():
    with open(SEQUENCES_FILE, 'r') as f:
        seqs = json.load(f)

    kmers = [a+b+c for a in 'ACGT' for b in 'ACGT' for c in 'ACGT']
    profiles = []

    # Needs to match the order in fit_model.py, but dict order in Python 3.7+ is insertion order.
    # The setup generates seq_1, seq_2, seq_target in that order.
    for seq_id, seq in seqs.items():
        profile = [seq.count(k) for k in kmers]
        profiles.append(profile)

    profiles_arr = np.array(profiles).T
    cov = np.cov(profiles_arr)

    # Add ridge penalty
    cov_reg = cov + 1e-5 * np.eye(cov.shape[0])
    L = np.linalg.cholesky(cov_reg)
    diag_L = np.diag(L)

    ref_dist = np.load(REF_DIST_FILE)

    return wasserstein_distance(diag_L, ref_dist)

def test_results_file_exists():
    assert os.path.isfile(RESULTS_FILE), f"Results file not found at {RESULTS_FILE}"

def test_results_format_and_values():
    with open(RESULTS_FILE, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not valid JSON"

    assert "best_seq_id" in res, "Missing 'best_seq_id' in results.json"
    assert "wasserstein_distance" in res, "Missing 'wasserstein_distance' in results.json"
    assert "primer_sequence" in res, "Missing 'primer_sequence' in results.json"

    assert res['best_seq_id'] == 'seq_target', f"Expected best_seq_id to be 'seq_target', got {res['best_seq_id']}"
    assert res['primer_sequence'] == 'ATGCGTACGTAGCTAGCTAG', f"Expected primer_sequence to be 'ATGCGTACGTAGCTAGCTAG', got {res['primer_sequence']}"

    expected_wd = compute_expected_wasserstein()
    actual_wd = res['wasserstein_distance']

    error = abs(actual_wd - expected_wd)
    threshold = 1e-4
    assert error <= threshold, f"Wasserstein distance error {error} exceeds threshold {threshold}. Expected approx {expected_wd}, got {actual_wd}"