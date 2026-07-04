# test_final_state.py

import os
import json
import shutil
import subprocess
import tempfile
import pytest

def test_filter_go_exists():
    assert os.path.isfile("/home/user/filter.go"), "The Go program /home/user/filter.go was not found."

def test_clean_corpus_processing():
    clean_dir = "/home/user/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    with tempfile.TemporaryDirectory() as output_dir:
        result = subprocess.run(
            ["go", "run", "/home/user/filter.go", clean_dir, output_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Go program failed on clean corpus. Error: {result.stderr}"

        output_files = set(os.listdir(output_dir))

        failed_clean = []
        for cf in clean_files:
            expected_out = f"{cf}.json"
            if expected_out not in output_files:
                failed_clean.append(cf)
                continue

            # Verify JSON content
            try:
                with open(os.path.join(output_dir, expected_out), 'r') as f:
                    data = json.load(f)
                if "config_data" not in data:
                    failed_clean.append(cf)
            except Exception:
                failed_clean.append(cf)

        if failed_clean:
            pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_clean)}")

def test_evil_corpus_processing():
    evil_dir = "/home/user/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    with tempfile.TemporaryDirectory() as output_dir:
        result = subprocess.run(
            ["go", "run", "/home/user/filter.go", evil_dir, output_dir],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Go program failed on evil corpus. Error: {result.stderr}"

        output_files = set(os.listdir(output_dir))

        bypassed_evil = []
        for ef in evil_files:
            expected_out = f"{ef}.json"
            if expected_out in output_files:
                bypassed_evil.append(ef)

        if bypassed_evil:
            pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_evil)}")