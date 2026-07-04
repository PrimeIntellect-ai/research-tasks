# test_final_state.py
import os
import subprocess
import pytest

CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"
EXECUTABLE = "/app/build/mathscript"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS):
        pytest.fail(f"Clean corpus directory missing at {CLEAN_CORPUS}")

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "No clean files found"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([EXECUTABLE, "verify", f], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "SAFE":
            failed_files.append((os.path.basename(f), result.returncode, result.stdout.strip()))

    if failed_files:
        msg = f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected.\n"
        msg += "Offending files:\n" + "\n".join([f"{name}: exit={code}, out={out}" for name, code, out in failed_files[:10]])
        pytest.fail(msg)

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS):
        pytest.fail(f"Evil corpus directory missing at {EVIL_CORPUS}")

    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "No evil files found"

    failed_files = []
    for f in evil_files:
        result = subprocess.run([EXECUTABLE, "verify", f], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "UNSAFE":
            failed_files.append((os.path.basename(f), result.returncode, result.stdout.strip()))

    if failed_files:
        msg = f"{len(failed_files)} of {len(evil_files)} evil files bypassed.\n"
        msg += "Offending files:\n" + "\n".join([f"{name}: exit={code}, out={out}" for name, code, out in failed_files[:10]])
        pytest.fail(msg)

def test_memory_leaks_valgrind():
    if not os.path.isdir(CLEAN_CORPUS):
        pytest.fail(f"Clean corpus directory missing at {CLEAN_CORPUS}")

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "No clean files found for valgrind test"

    sample_file = clean_files[0]
    result = subprocess.run(
        ["valgrind", "--error-exitcode=255", "--leak-check=full", EXECUTABLE, "eval", sample_file],
        capture_output=True, text=True
    )

    assert result.returncode == 0, f"Valgrind reported memory leaks or errors (exit code {result.returncode}):\n{result.stderr}"