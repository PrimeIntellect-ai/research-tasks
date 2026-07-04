# test_final_state.py

import os
import json
import timeit
import pytest
from passlib.hash import md5_crypt

def test_audit_script_modified():
    """Check that the audit script no longer accepts passwords via CLI."""
    path = "/home/user/audit.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "--passwords" not in content, "Audit script still contains '--passwords' CLI argument."
    assert "argparse" not in content or "add_argument('--passwords'" not in content, "Audit script still accepts passwords via CLI."

def test_cracked_json():
    """Check that cracked.json exists, is valid, and contains correct cracks."""
    json_path = "/home/user/cracked.json"
    hashes_path = "/home/user/legacy_hashes.txt"

    assert os.path.isfile(json_path), f"File {json_path} is missing. The script did not generate the output."
    assert os.path.isfile(hashes_path), f"File {hashes_path} is missing."

    with open(hashes_path, "r") as f:
        legacy_hashes = [line.strip() for line in f if line.strip()]

    with open(json_path, "r") as f:
        try:
            cracked = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert isinstance(cracked, dict), "cracked.json must contain a JSON object (dictionary)."
    assert len(cracked) > 0, "cracked.json is empty. No hashes were cracked."

    for h, p in cracked.items():
        assert h in legacy_hashes, f"Hash {h} in cracked.json was not found in legacy_hashes.txt"
        assert isinstance(p, str), f"Cracked password for {h} is not a string."
        # Verify that the cracked password actually matches the hash
        assert md5_crypt.verify(p, h), f"Password '{p}' does not correctly verify against hash {h}."

def test_speedup_metric():
    """Check the execution speedup of md5_crypt.verify() against the baseline."""
    setup_code = "from passlib.hash import md5_crypt; h = md5_crypt.hash('secret')"
    test_code = "md5_crypt.verify('secret', h)"

    # Time for 50 iterations
    try:
        new_time = timeit.timeit(test_code, setup=setup_code, number=50)
    except Exception as e:
        pytest.fail(f"Failed to benchmark md5_crypt.verify: {e}")

    # Baseline time for perturbed library: 50 * 0.05s = 2.5s
    baseline_time = 2.5
    speedup = baseline_time / new_time

    assert speedup >= 20.0, (
        f"Performance bottleneck not fully resolved. "
        f"Achieved speedup: {speedup:.2f}x (Threshold >= 20.0x). "
        f"Time taken for 50 iterations: {new_time:.4f}s."
    )