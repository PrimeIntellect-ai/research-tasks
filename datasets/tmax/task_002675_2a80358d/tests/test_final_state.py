# test_final_state.py

import os
import subprocess
import tempfile
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
FILTER_CLI = "/home/user/filter_cli"

def test_filter_cli_exists_and_executable():
    assert os.path.isfile(FILTER_CLI), f"Filter CLI binary not found at {FILTER_CLI}"
    assert os.access(FILTER_CLI, os.X_OK), f"Filter CLI at {FILTER_CLI} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_failed = []
    evil_failed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test clean corpus
        for cfile in clean_files:
            input_path = os.path.join(CLEAN_CORPUS_DIR, cfile)
            output_path = os.path.join(tmpdir, f"out_{cfile}")

            result = subprocess.run([FILTER_CLI, input_path, output_path], capture_output=True)
            if result.returncode != 0:
                clean_failed.append(cfile)
                continue

            if not os.path.exists(output_path):
                clean_failed.append(cfile)
                continue

            with open(input_path, 'r') as f_in, open(output_path, 'r') as f_out:
                in_lines = f_in.readlines()
                out_lines = f_out.readlines()

            if in_lines != out_lines:
                clean_failed.append(cfile)

        # Test evil corpus
        for efile in evil_files:
            input_path = os.path.join(EVIL_CORPUS_DIR, efile)
            output_path = os.path.join(tmpdir, f"out_{efile}")

            result = subprocess.run([FILTER_CLI, input_path, output_path], capture_output=True)
            if result.returncode != 0:
                # Failing gracefully is acceptable, but output must be empty if it succeeds
                pass
            elif os.path.exists(output_path):
                with open(output_path, 'r') as f_out:
                    out_lines = f_out.readlines()
                if len(out_lines) > 0:
                    evil_failed.append(efile)

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))