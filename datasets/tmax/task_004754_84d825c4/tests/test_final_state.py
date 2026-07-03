# test_final_state.py

import os
import difflib
import string

def test_credential_rotation():
    new_key_path = "/home/user/new_key.txt"
    assert os.path.exists(new_key_path), f"File {new_key_path} does not exist."

    with open(new_key_path, "r") as f:
        new_key = f.read().strip()

    assert len(new_key) == 16, f"New key must be exactly 16 characters long, got {len(new_key)}."
    assert all(c in string.ascii_letters + string.digits for c in new_key), "New key must be alphanumeric."

def test_metric_threshold():
    score = 0.0

    # 1. Key Verification
    expected_key = "S3cr3tK3y123!@#"
    extracted_key_path = "/home/user/compromised_key.txt"
    assert os.path.exists(extracted_key_path), f"File {extracted_key_path} does not exist."

    with open(extracted_key_path, "r") as f:
        extracted_key = f.read().strip()

    similarity = difflib.SequenceMatcher(None, expected_key, extracted_key).ratio()
    score += 0.5 * similarity

    # 2. CSP Verification
    csp_path = "/home/user/strict_csp.txt"
    assert os.path.exists(csp_path), f"File {csp_path} does not exist."

    with open(csp_path, "r") as f:
        csp = f.read().strip().lower()

    csp_score = 0.0
    if "default-src 'self'" in csp: 
        csp_score += 0.1
    if "script-src" in csp and "'self'" in csp and "https://scripts.trusted.internal" in csp: 
        csp_score += 0.2
    if "unsafe-inline" not in csp and "unsafe-eval" not in csp: 
        csp_score += 0.1
    if "object-src 'none'" in csp: 
        csp_score += 0.1

    score += min(0.5, csp_score)

    threshold = 0.90
    assert score >= threshold, f"Score {score:.2f} is below the threshold of {threshold:.2f}. Key similarity: {similarity:.2f}, CSP score: {csp_score:.2f}"