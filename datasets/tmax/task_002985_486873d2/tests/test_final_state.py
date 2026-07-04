# test_final_state.py
import os
import glob
import subprocess
import pytest

BINARY_DIR = "/home/user/cypher_filter"
BINARY_PATH = "/home/user/cypher_filter/target/release/cypher_filter"

@pytest.fixture(scope="module", autouse=True)
def build_rust_project():
    """Ensure the Rust project is built before running tests."""
    if os.path.isdir(BINARY_DIR) and os.path.isfile(os.path.join(BINARY_DIR, "Cargo.toml")):
        subprocess.run(["cargo", "build", "--release"], cwd=BINARY_DIR, capture_output=True)

def test_rust_project_exists():
    assert os.path.isdir(BINARY_DIR), f"Rust project directory {BINARY_DIR} does not exist."
    assert os.path.isfile(os.path.join(BINARY_DIR, "Cargo.toml")), "Cargo.toml not found in the project directory."
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Ensure it compiles successfully."

def test_clean_corpus_accepted():
    clean_files = glob.glob("/app/corpus/clean/*.cypher")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_clean = []
    for f in clean_files:
        res = subprocess.run([BINARY_PATH, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected (expected exit 0): {', '.join(failed_clean)}"

def test_evil_corpus_rejected():
    evil_files = glob.glob("/app/corpus/evil/*.cypher")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_evil = []
    for f in evil_files:
        res = subprocess.run([BINARY_PATH, f], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(f))

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil bypassed (expected exit 1): {', '.join(failed_evil)}"