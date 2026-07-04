# test_final_state.py

import os
import subprocess
import pytest

VERIFIER_SCRIPT = '/home/user/verifier.py'
EVAL_CLEAN_DIR = '/app/eval/clean/'
EVAL_EVIL_DIR = '/app/eval/evil/'

def run_verifier(directory):
    result = subprocess.run(['python3', VERIFIER_SCRIPT, directory], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    results = {}
    for line in result.stdout.strip().split('\n'):
        if not line.strip():
            continue
        if ': ' in line:
            filename, status = line.split(': ', 1)
            results[filename.strip()] = status.strip()
    return results

def test_verifier_script_exists():
    assert os.path.isfile(VERIFIER_SCRIPT), f"Verifier script not found at {VERIFIER_SCRIPT}"

def test_clean_corpus_accepted():
    results = run_verifier(EVAL_CLEAN_DIR)
    expected_files = sorted([f for f in os.listdir(EVAL_CLEAN_DIR) if f.endswith('.zip')])

    rejected = []
    for f in expected_files:
        if f not in results:
            rejected.append(f"{f} (missing from output)")
        elif results[f] != 'ACCEPT':
            rejected.append(f"{f} (got {results[f]})")

    assert not rejected, f"{len(rejected)} of {len(expected_files)} clean files modified/rejected:\n" + "\n".join(rejected)

def test_evil_corpus_rejected():
    results = run_verifier(EVAL_EVIL_DIR)
    expected_files = sorted([f for f in os.listdir(EVAL_EVIL_DIR) if f.endswith('.zip')])

    accepted = []
    for f in expected_files:
        if f not in results:
            accepted.append(f"{f} (missing from output)")
        elif results[f] != 'REJECT':
            accepted.append(f"{f} (got {results[f]})")

    assert not accepted, f"{len(accepted)} of {len(expected_files)} evil files bypassed:\n" + "\n".join(accepted)