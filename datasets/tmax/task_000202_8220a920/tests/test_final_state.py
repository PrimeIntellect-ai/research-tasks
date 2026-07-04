# test_final_state.py

import os
import subprocess
import pytest

def test_extractor_built():
    extractor_path = "/app/graph-backup-extractor-v2.1.0/bin/extractor"
    assert os.path.isfile(extractor_path), f"Extractor binary not found at {extractor_path}. Did you run make build?"
    assert os.access(extractor_path, os.X_OK), f"Extractor binary at {extractor_path} is not executable."

def test_sanitizer_built():
    sanitizer_path = "/app/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer binary not found at {sanitizer_path}."
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer binary at {sanitizer_path} is not executable."

def test_sanitizer_clean_corpus():
    clean_dir = "/app/corpora/clean"
    sanitizer_path = "/app/sanitizer"

    if not os.path.isdir(clean_dir):
        pytest.skip(f"Clean corpus directory {clean_dir} missing.")

    files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    if not files:
        pytest.skip("No JSON files found in clean corpus.")

    result = subprocess.run([sanitizer_path, clean_dir], capture_output=True, text=True)
    output = result.stdout + "\n" + result.stderr

    rejected = []
    missing = []
    for f in files:
        if f"REJECTED: {f}" in output:
            rejected.append(f)
        elif f"ACCEPTED: {f}" not in output:
            missing.append(f)

    errors = []
    if rejected:
        errors.append(f"{len(rejected)} of {len(files)} clean files were incorrectly REJECTED: {', '.join(rejected[:5])}")
    if missing:
        errors.append(f"{len(missing)} of {len(files)} clean files were not ACCEPTED: {', '.join(missing[:5])}")

    assert not errors, "Clean corpus validation failed:\n" + "\n".join(errors)

def test_sanitizer_evil_corpus():
    evil_dir = "/app/corpora/evil"
    sanitizer_path = "/app/sanitizer"

    if not os.path.isdir(evil_dir):
        pytest.skip(f"Evil corpus directory {evil_dir} missing.")

    files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    if not files:
        pytest.skip("No JSON files found in evil corpus.")

    result = subprocess.run([sanitizer_path, evil_dir], capture_output=True, text=True)
    output = result.stdout + "\n" + result.stderr

    accepted = []
    missing = []
    for f in files:
        if f"ACCEPTED: {f}" in output:
            accepted.append(f)
        elif f"REJECTED: {f}" not in output:
            missing.append(f)

    errors = []
    if accepted:
        errors.append(f"{len(accepted)} of {len(files)} evil files bypassed and were ACCEPTED: {', '.join(accepted[:5])}")
    if missing:
        errors.append(f"{len(missing)} of {len(files)} evil files were not REJECTED: {', '.join(missing[:5])}")

    assert not errors, "Evil corpus validation failed:\n" + "\n".join(errors)