# test_final_state.py

import os
import subprocess
import pytest

CPP_SOURCE = "/home/user/url_sanitizer.cpp"
COMPILED_BINARY = "/home/user/sanitizer"
CLEAN_CORPUS = "/app/clean_urls.txt"
EVIL_CORPUS = "/app/evil_urls.txt"

def test_source_file_exists():
    assert os.path.isfile(CPP_SOURCE), f"The C++ source file {CPP_SOURCE} does not exist."

def test_compilation():
    compile_cmd = [
        "g++", "-std=c++17", "-O2", "-fsanitize=address", "-Wall",
        CPP_SOURCE, "-o", COMPILED_BINARY
    ]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"
    assert os.path.isfile(COMPILED_BINARY), f"Compiled binary {COMPILED_BINARY} was not created."

def test_adversarial_corpus():
    # Ensure compilation happened
    if not os.path.isfile(COMPILED_BINARY):
        pytest.fail("Compiled binary missing, cannot run corpus tests.")

    with open(CLEAN_CORPUS, "r") as f:
        clean_urls = [line.strip() for line in f if line.strip()]

    with open(EVIL_CORPUS, "r") as f:
        evil_urls = [line.strip() for line in f if line.strip()]

    clean_failures = []
    evil_failures = []
    asan_errors = []

    # Test clean URLs
    for url in clean_urls:
        result = subprocess.run([COMPILED_BINARY, url], capture_output=True, text=True)
        if "ERROR: AddressSanitizer" in result.stderr:
            asan_errors.append(url)
        elif result.returncode != 0:
            clean_failures.append(url)

    # Test evil URLs
    for url in evil_urls:
        result = subprocess.run([COMPILED_BINARY, url], capture_output=True, text=True)
        if "ERROR: AddressSanitizer" in result.stderr:
            asan_errors.append(url)
        elif result.returncode == 0:
            evil_failures.append(url)

    error_msg = []
    if asan_errors:
        error_msg.append(f"{len(asan_errors)} URLs triggered AddressSanitizer errors.")
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_urls)} clean URLs modified/rejected: {clean_failures}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_urls)} evil URLs bypassed/accepted: {evil_failures}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))