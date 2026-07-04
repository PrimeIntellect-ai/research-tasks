# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import pytest

SCRIPT_PATH = "/home/user/ingest_filter.py"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

@pytest.fixture(scope="module")
def run_clean():
    out_dir = tempfile.mkdtemp()
    strace_log = tempfile.mktemp()
    cmd = [
        "strace", "-f", "-e", "trace=rename,renameat2", "-o", strace_log,
        "python3", SCRIPT_PATH, "--input-dir", CLEAN_CORPUS, "--output-dir", out_dir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    yield out_dir, strace_log, result
    shutil.rmtree(out_dir, ignore_errors=True)
    if os.path.exists(strace_log):
        os.remove(strace_log)

@pytest.fixture(scope="module")
def run_evil():
    out_dir = tempfile.mkdtemp()
    cmd = [
        "python3", SCRIPT_PATH, "--input-dir", EVIL_CORPUS, "--output-dir", out_dir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    yield out_dir, result
    shutil.rmtree(out_dir, ignore_errors=True)

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Ingestion script missing at {SCRIPT_PATH}"

def test_clean_corpus(run_clean):
    out_dir, strace_log, result = run_clean

    assert result.returncode == 0, f"Script failed on clean corpus with error: {result.stderr}"

    expected_files = set(f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.zip'))
    output_files = set(f for f in os.listdir(out_dir) if f.endswith('.zip'))

    missing = expected_files - output_files
    modified = output_files - expected_files

    assert not missing, f"{len(missing)} of {len(expected_files)} clean files were incorrectly rejected. Missing: {missing}"
    assert not modified, f"Unexpected files generated in output directory: {modified}"

    # Check atomic rename requirement
    assert os.path.exists(strace_log), "strace log was not created."
    with open(strace_log, 'r') as f:
        log_content = f.read()

    # We expect to see a rename operation from a .tmp file to a .zip file
    assert ".tmp" in log_content and ".zip" in log_content, (
        "Atomic rename requirement not met. No rename syscalls moving .tmp to .zip found in strace log."
    )

def test_evil_corpus(run_evil):
    out_dir, result = run_evil

    assert result.returncode == 0, f"Script failed on evil corpus with error: {result.stderr}"

    expected_evil_files = set(f for f in os.listdir(EVIL_CORPUS) if f.endswith('.zip'))
    output_files = set(f for f in os.listdir(out_dir) if f.endswith('.zip'))

    assert not output_files, f"{len(output_files)} of {len(expected_evil_files)} evil files bypassed the filter and were written to output: {output_files}"