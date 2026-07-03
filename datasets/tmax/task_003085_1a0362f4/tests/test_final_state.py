# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/validator/target/release/validator"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_validator_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"The compiled binary does not exist at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"The file at {BINARY_PATH} is not executable"

def test_adversarial_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.fail("Validator binary not found, cannot run corpus tests.")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_failures = []
    for filepath in clean_files:
        try:
            result = subprocess.run(
                [BINARY_PATH, filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_failures.append((os.path.basename(filepath), output))
        except Exception as e:
            clean_failures.append((os.path.basename(filepath), str(e)))

    evil_failures = []
    for filepath in evil_files:
        try:
            result = subprocess.run(
                [BINARY_PATH, filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "REJECT":
                evil_failures.append((os.path.basename(filepath), output))
        except Exception as e:
            evil_failures.append((os.path.basename(filepath), str(e)))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected. Offending files: " + ", ".join([f[0] for f in clean_failures]))
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted. Offending files: " + ", ".join([f[0] for f in evil_failures]))

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_fast_solver_compiles_now():
    # Verify that the fast_solver package's Cargo.toml was fixed.
    cargo_toml_path = "/app/fast_solver/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), "fast_solver Cargo.toml is missing."
    with open(cargo_toml_path, "r") as f:
        content = f.read()
    assert 'serde = "1.99.0"' not in content, "The invalid serde version '1.99.0' is still in /app/fast_solver/Cargo.toml"