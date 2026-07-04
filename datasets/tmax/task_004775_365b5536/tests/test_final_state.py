# test_final_state.py
import os
import json
import hashlib
import subprocess

def test_curator_script():
    script_path = "/home/user/curator.py"
    assert os.path.exists(script_path), f"Script {script_path} not found."

    clean_in = "/app/corpus/clean"
    clean_out = "/tmp/out_clean"
    evil_in = "/app/corpus/evil"
    evil_out = "/tmp/out_evil"

    os.makedirs(clean_out, exist_ok=True)
    os.makedirs(evil_out, exist_ok=True)

    # Run on clean corpus
    res_clean = subprocess.run(["python3", script_path, clean_in, clean_out], capture_output=True, text=True)
    assert res_clean.returncode == 0, f"Script failed on clean corpus. stderr: {res_clean.stderr}"

    # Run on evil corpus
    res_evil = subprocess.run(["python3", script_path, evil_in, evil_out], capture_output=True, text=True)
    assert res_evil.returncode == 0, f"Script failed on evil corpus. stderr: {res_evil.stderr}"

    # Validate clean corpus results
    clean_files = [f for f in os.listdir(clean_in) if f.endswith('.fw')]
    out_clean_files = [f for f in os.listdir(clean_out) if f.endswith('.fw')]

    missing_clean = set(clean_files) - set(out_clean_files)
    assert not missing_clean, f"{len(missing_clean)} of {len(clean_files)} clean files modified or rejected: {missing_clean}"

    manifest_clean_path = os.path.join(clean_out, "manifest.json")
    assert os.path.exists(manifest_clean_path), "manifest.json missing in clean output directory."

    with open(manifest_clean_path, 'r') as f:
        try:
            manifest_clean = json.load(f)
        except json.JSONDecodeError:
            assert False, "manifest.json in clean output is not valid JSON."

    for cf in clean_files:
        assert cf in manifest_clean, f"{cf} is missing from the clean manifest.json."

        with open(os.path.join(clean_in, cf), 'rb') as f:
            expected_hash = hashlib.sha256(f.read()).hexdigest()
        assert manifest_clean[cf] == expected_hash, f"SHA256 hash mismatch for {cf} in manifest.json."

    # Validate evil corpus results
    evil_files = [f for f in os.listdir(evil_in) if f.endswith('.fw')]
    out_evil_files = [f for f in os.listdir(evil_out) if f.endswith('.fw')]

    assert not out_evil_files, f"{len(out_evil_files)} of {len(evil_files)} evil files bypassed rejection: {out_evil_files}"

    manifest_evil_path = os.path.join(evil_out, "manifest.json")
    if os.path.exists(manifest_evil_path):
        with open(manifest_evil_path, 'r') as f:
            try:
                manifest_evil = json.load(f)
            except json.JSONDecodeError:
                assert False, "manifest.json in evil output is not valid JSON."

        assert not manifest_evil, f"manifest.json in evil output should be empty, but contains: {manifest_evil}"