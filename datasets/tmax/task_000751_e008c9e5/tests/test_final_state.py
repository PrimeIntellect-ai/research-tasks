# test_final_state.py

import os
import subprocess
import pytest

def test_vendor_compilation():
    vendor_dir = "/app/vendor/libcsvquery"

    # Run make in the vendor directory
    result = subprocess.run(["make", "-C", vendor_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"make failed in {vendor_dir}:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Check if the static library was produced
    lib_path = os.path.join(vendor_dir, "libcsvquery.a")
    assert os.path.isfile(lib_path), f"Expected static library {lib_path} was not created."

def test_sanitizer_executable_exists():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer executable {sanitizer_path} is missing."
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer {sanitizer_path} is not executable."

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run([sanitizer_path, filepath], capture_output=True, text=True)

        if result.returncode != 0 or result.stdout != "CLEAN\n":
            failed_files.append((filename, result.stdout.strip(), result.stderr.strip()))

    if failed_files:
        details = "\n".join([f"{f}: stdout='{out}', stderr='{err}'" for f, out, err in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected:\n{details}")

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitizer"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run([sanitizer_path, filepath], capture_output=True, text=True)

        if result.returncode != 0 or result.stdout != "EVIL\n":
            failed_files.append((filename, result.stdout.strip(), result.stderr.strip()))

    if failed_files:
        details = "\n".join([f"{f}: stdout='{out}', stderr='{err}'" for f, out, err in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed:\n{details}")