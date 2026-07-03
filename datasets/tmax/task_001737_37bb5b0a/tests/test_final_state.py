# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/telemetry_gate/target/release/telemetry_gate"
CLEAN_CORPUS_DIR = "/home/user/corpora/clean/"
EVIL_CORPUS_DIR = "/home/user/corpora/evil/"
BENCHMARK_RESULTS_FILE = "/home/user/benchmark_results.txt"

def test_rust_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Rust binary not found at {BINARY_PATH}. Did you run 'cargo build --release'?"
    assert os.access(BINARY_PATH, os.X_OK), f"Rust binary at {BINARY_PATH} is not executable."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing at {CLEAN_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    failures = []
    for f in clean_files:
        file_path = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run([BINARY_PATH, file_path], capture_output=True)
        if result.returncode != 0:
            failures.append(f)

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files rejected (expected accepted/exit 0). Offending files: {failures[:5]}...")

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing at {EVIL_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    failures = []
    for f in evil_files:
        file_path = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run([BINARY_PATH, file_path], capture_output=True)
        if result.returncode == 0:
            failures.append(f)

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed (expected rejected/exit != 0). Offending files: {failures[:5]}...")

def test_benchmark_results():
    assert os.path.isfile(BENCHMARK_RESULTS_FILE), f"Benchmark results file missing at {BENCHMARK_RESULTS_FILE}"

    with open(BENCHMARK_RESULTS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content.strip()) > 0, f"Benchmark results file {BENCHMARK_RESULTS_FILE} is empty."
    assert "Benchmark completed" in content, f"Benchmark results file {BENCHMARK_RESULTS_FILE} does not contain 'Benchmark completed'."