# test_final_state.py

import os
import json
import re
import subprocess
import tempfile
import pytest

def normalize_payload(payload: str) -> str:
    # Convert to lowercase, strip all whitespace, prepend 'cfg_'
    no_whitespace = re.sub(r'\s+', '', payload)
    return f"cfg_{no_whitespace.lower()}"

def compute_expected_records(records):
    # 1. Impute timestamps
    # Group by host to find previous and next valid
    hosts_records = {}
    for i, r in enumerate(records):
        host = r['host']
        if host not in hosts_records:
            hosts_records[host] = []
        hosts_records[host].append((i, r))

    for host, host_recs in hosts_records.items():
        for idx, (orig_i, r) in enumerate(host_recs):
            if r['ts'] == 0:
                prev_ts = host_recs[idx-1][1]['ts']
                next_ts = host_recs[idx+1][1]['ts']
                r['ts'] = (prev_ts + next_ts) // 2

    # 2. Windowed Deduplication
    accepted = []
    # keep track of accepted per host
    last_accepted = {} # host -> list of (ts, norm_payload)

    for r in records:
        host = r['host']
        ts = r['ts']
        norm_payload = normalize_payload(r['config_payload'])

        if host not in last_accepted:
            last_accepted[host] = []

        is_dup = False
        # check against previously accepted for the same host
        for prev_ts, prev_norm in reversed(last_accepted[host]):
            if ts - prev_ts <= 120:
                if norm_payload == prev_norm:
                    is_dup = True
                    break

        if not is_dup:
            last_accepted[host].append((ts, norm_payload))
            accepted.append(r)

    return accepted

def read_jsonl(path):
    with open(path, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def test_sanitizer_executable_exists():
    assert os.path.isfile("/home/user/sanitizer.go"), "sanitizer.go is missing"

def test_adversarial_corpus():
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".jsonl")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".jsonl")]

    clean_modified = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean corpus
        for cfile in clean_files:
            basename = os.path.basename(cfile)
            out_path = os.path.join(tmpdir, f"out_{basename}")

            result = subprocess.run(["go", "run", "/home/user/sanitizer.go", cfile, out_path], capture_output=True)
            if result.returncode != 0 or not os.path.exists(out_path):
                clean_modified.append(basename)
                continue

            input_records = read_jsonl(cfile)
            output_records = read_jsonl(out_path)

            if input_records != output_records:
                clean_modified.append(basename)

        # Test evil corpus
        for efile in evil_files:
            basename = os.path.basename(efile)
            out_path = os.path.join(tmpdir, f"out_{basename}")

            result = subprocess.run(["go", "run", "/home/user/sanitizer.go", efile, out_path], capture_output=True)
            if result.returncode != 0 or not os.path.exists(out_path):
                evil_bypassed.append(basename)
                continue

            input_records = read_jsonl(efile)
            expected_records = compute_expected_records(input_records)
            output_records = read_jsonl(out_path)

            if expected_records != output_records:
                evil_bypassed.append(basename)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))