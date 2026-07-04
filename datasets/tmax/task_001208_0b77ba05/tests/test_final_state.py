# test_final_state.py

import os
import subprocess
import pytest

CLEAN_DIR = "/home/user/data/clean"
EVIL_DIR = "/home/user/data/evil"
EXECUTABLE = "/home/user/sequence_sanitizer"
LIB_PATH = "/app/libfasta-parser/libfasta.so"

def test_libfasta_compiled():
    assert os.path.isfile(LIB_PATH), f"Shared library {LIB_PATH} was not compiled."

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} not found."
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_adversarial_corpus():
    if not os.path.isfile(EXECUTABLE):
        pytest.fail(f"Executable {EXECUTABLE} not found.")

    env = os.environ.copy()
    # Ensure the shared library can be found if not compiled with rpath
    env["LD_LIBRARY_PATH"] = "/app/libfasta-parser:" + env.get("LD_LIBRARY_PATH", "")

    clean_files = sorted([os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.fasta')])
    evil_files = sorted([os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.fasta')])

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}"

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        with open(cf, 'rb') as f:
            input_data = f.read()

        try:
            result = subprocess.run([EXECUTABLE], input=input_data, env=env, capture_output=True, timeout=2)
            if result.stdout != input_data:
                clean_modified.append(os.path.basename(cf))
        except subprocess.TimeoutExpired:
            clean_modified.append(os.path.basename(cf) + " (timeout)")
        except Exception as e:
            clean_modified.append(os.path.basename(cf) + f" (error)")

    for ef in evil_files:
        with open(ef, 'rb') as f:
            input_data = f.read()

        try:
            result = subprocess.run([EXECUTABLE], input=input_data, env=env, capture_output=True, timeout=2)
            if result.stdout.strip():
                evil_bypassed.append(os.path.basename(ef))
        except subprocess.TimeoutExpired:
            evil_bypassed.append(os.path.basename(ef) + " (timeout)")
        except Exception as e:
            evil_bypassed.append(os.path.basename(ef) + f" (error)")

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))