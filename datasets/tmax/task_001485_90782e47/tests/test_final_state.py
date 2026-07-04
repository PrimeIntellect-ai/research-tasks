# test_final_state.py

import os
import subprocess
import pytest
from pathlib import Path

def test_libparser_built():
    """Verify that libparser.so was built successfully."""
    so_path = "/app/libparser/libparser.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} is missing. Did the Makefile build succeed?"

def test_validator_exists_and_linked():
    """Verify that the validator executable exists and is linked against libparser.so."""
    validator_path = "/app/validator"
    assert os.path.isfile(validator_path), f"Validator executable {validator_path} is missing."
    assert os.access(validator_path, os.X_OK), f"Validator executable {validator_path} is not executable."

    try:
        ldd_output = subprocess.check_output(["ldd", validator_path], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ldd on {validator_path}: {e}")

    assert "libparser.so" in ldd_output, f"Validator is not linked against libparser.so. ldd output: {ldd_output}"

def test_validator_clean_corpus():
    """Verify that the validator accepts all files in the clean corpus."""
    clean_dir = Path("/app/corpus/clean")
    assert clean_dir.is_dir(), f"Clean corpus directory {clean_dir} is missing."

    clean_files = list(clean_dir.iterdir())
    assert clean_files, "Clean corpus is empty."

    failed_files = []
    for f in clean_files:
        if not f.is_file():
            continue
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/app/libparser:" + env.get("LD_LIBRARY_PATH", "")
        result = subprocess.run(["/app/validator", str(f)], env=env, capture_output=True)
        if result.returncode != 0:
            failed_files.append(f.name)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_validator_evil_corpus():
    """Verify that the validator rejects all files in the evil corpus."""
    evil_dir = Path("/app/corpus/evil")
    assert evil_dir.is_dir(), f"Evil corpus directory {evil_dir} is missing."

    evil_files = list(evil_dir.iterdir())
    assert evil_files, "Evil corpus is empty."

    bypassed_files = []
    for f in evil_files:
        if not f.is_file():
            continue
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/app/libparser:" + env.get("LD_LIBRARY_PATH", "")
        result = subprocess.run(["/app/validator", str(f)], env=env, capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(f.name)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(bypassed_files)}")