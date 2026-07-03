# test_final_state.py
import os
import subprocess
import tempfile
import filecmp
import shutil
import pytest

EXECUTABLE = "/home/user/log_filter"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_clean_corpus_preserved():
    """Test that all clean corpus files are preserved and unchanged."""
    out_dir = tempfile.mkdtemp()
    try:
        result = subprocess.run([EXECUTABLE, CLEAN_CORPUS, out_dir], capture_output=True, text=True)
        assert result.returncode == 0, f"Executable failed on clean corpus with return code {result.returncode}\nStderr: {result.stderr}"

        clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
        missing = []
        modified = []

        for f in clean_files:
            src = os.path.join(CLEAN_CORPUS, f)
            dst = os.path.join(out_dir, f)
            if not os.path.isfile(dst):
                missing.append(f)
            elif not filecmp.cmp(src, dst, shallow=False):
                modified.append(f)

        errors = []
        if missing:
            errors.append(f"{len(missing)} of {len(clean_files)} clean files missing: {missing}")
        if modified:
            errors.append(f"{len(modified)} of {len(clean_files)} clean files modified: {modified}")

        assert not errors, "\n".join(errors)
    finally:
        shutil.rmtree(out_dir)

def test_evil_corpus_rejected():
    """Test that all evil corpus files are rejected."""
    out_dir = tempfile.mkdtemp()
    try:
        result = subprocess.run([EXECUTABLE, EVIL_CORPUS, out_dir], capture_output=True, text=True)
        assert result.returncode == 0, f"Executable failed on evil corpus with return code {result.returncode}\nStderr: {result.stderr}"

        evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
        bypassed = []

        for f in evil_files:
            dst = os.path.join(out_dir, f)
            if os.path.isfile(dst):
                bypassed.append(f)

        if bypassed:
            pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil files bypassed (copied to output): {bypassed}")
    finally:
        shutil.rmtree(out_dir)