# test_final_state.py

import os
import subprocess
import sys

def test_filter_script_exists():
    assert os.path.isfile('/home/user/filter.py'), "/home/user/filter.py does not exist."

def test_filter_on_evil_corpus():
    evil_dir = '/verifier/corpora/evil/'
    if not os.path.exists(evil_dir):
        # If corpus doesn't exist, we can't test it, but assume it's created by the environment
        return

    evil_files = {f for f in os.listdir(evil_dir) if f.endswith('.dat')}

    result = subprocess.run(
        [sys.executable, '/home/user/filter.py', evil_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on evil corpus with error: {result.stderr}"

    output_lines = {line.strip() for line in result.stdout.strip().split('\n') if line.strip()}

    bypassed = evil_files.intersection(output_lines)
    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil files bypassed. Offending files: {', '.join(bypassed)}"

def test_filter_on_clean_corpus():
    clean_dir = '/verifier/corpora/clean/'
    if not os.path.exists(clean_dir):
        return

    clean_files = {f for f in os.listdir(clean_dir) if f.endswith('.dat')}

    result = subprocess.run(
        [sys.executable, '/home/user/filter.py', clean_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on clean corpus with error: {result.stderr}"

    output_lines = {line.strip() for line in result.stdout.strip().split('\n') if line.strip()}

    missing = clean_files - output_lines
    modified_or_missing = len(missing)

    assert not missing, f"{modified_or_missing} of {len(clean_files)} clean files modified/rejected. Offending files: {', '.join(missing)}"