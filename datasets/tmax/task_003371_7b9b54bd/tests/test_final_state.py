# test_final_state.py
import os
import subprocess
import pytest

BINARY_PATH = "/home/user/sequence_filter/target/release/sequence_filter"
EVIL_CORPUS = "/app/corpus/evil"
CLEAN_CORPUS = "/app/corpus/clean"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Rust binary not found at {BINARY_PATH}. Did you compile it in release mode?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def run_classifier(corpus_path):
    result = subprocess.run(
        [BINARY_PATH, corpus_path],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, f"Binary failed with return code {result.returncode}. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    parsed_results = {}
    for line in output_lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid output format: '{line}'. Expected 'filename.fasta,STATUS'"
        filename, status = parts[0].strip(), parts[1].strip()
        parsed_results[filename] = status

    return parsed_results

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith(".fasta")]
    assert len(evil_files) > 0, "No FASTA files found in evil corpus."

    results = run_classifier(EVIL_CORPUS)

    bypassed = []
    for f in evil_files:
        if f not in results:
            bypassed.append(f"{f} (missing in output)")
        elif results[f] != "EVIL":
            bypassed.append(f"{f} (classified as {results[f]})")

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed)}"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith(".fasta")]
    assert len(clean_files) > 0, "No FASTA files found in clean corpus."

    results = run_classifier(CLEAN_CORPUS)

    modified = []
    for f in clean_files:
        if f not in results:
            modified.append(f"{f} (missing in output)")
        elif results[f] != "CLEAN":
            modified.append(f"{f} (classified as {results[f]})")

    assert not modified, f"{len(modified)} of {len(clean_files)} clean files modified/rejected: {', '.join(modified)}"