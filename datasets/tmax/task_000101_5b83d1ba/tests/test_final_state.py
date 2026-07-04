# test_final_state.py

import os
import subprocess
import json
import pytest
import shutil

CONVERTER_GO = "/home/user/converter.go"
LEGACY_PARSER = "/app/legacy_parser"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
COMPILED_BIN = "/tmp/converter_bin"

@pytest.fixture(scope="session", autouse=True)
def compile_go_program():
    assert os.path.exists(CONVERTER_GO), f"Missing required file: {CONVERTER_GO}"
    # Compile the Go program once to speed up testing
    result = subprocess.run(
        ["go", "build", "-o", COMPILED_BIN, CONVERTER_GO],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to compile {CONVERTER_GO}:\n{result.stderr}"
    yield
    if os.path.exists(COMPILED_BIN):
        os.remove(COMPILED_BIN)

def test_clean_corpus():
    clean_files = [
        os.path.join(CLEAN_CORPUS_DIR, f) 
        for f in os.listdir(CLEAN_CORPUS_DIR) 
        if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))
    ]

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    total = len(clean_files)

    for f in clean_files:
        out_file = "/tmp/out_clean.json"
        if os.path.exists(out_file):
            os.remove(out_file)

        result = subprocess.run([COMPILED_BIN, f, out_file], capture_output=True)

        if result.returncode != 0:
            failed_files.append((os.path.basename(f), f"Exit code {result.returncode}"))
            continue

        if not os.path.exists(out_file):
            failed_files.append((os.path.basename(f), "Output file not created"))
            continue

        # Get expected JSON from legacy parser
        legacy_result = subprocess.run([LEGACY_PARSER, f], capture_output=True, text=True)
        if legacy_result.returncode != 0:
            # If legacy parser fails on a clean file, it's a setup issue, but we skip or fail
            pass

        try:
            expected_json = json.loads(legacy_result.stdout)
        except json.JSONDecodeError:
            expected_json = None

        try:
            with open(out_file, 'r') as of:
                actual_json = json.load(of)
        except json.JSONDecodeError:
            failed_files.append((os.path.basename(f), "Output is not valid JSON"))
            continue

        if expected_json is not None and actual_json != expected_json:
            failed_files.append((os.path.basename(f), "JSON output does not match legacy parser"))
            continue

    if failed_files:
        details = ", ".join([f"{name} ({reason})" for name, reason in failed_files])
        pytest.fail(f"{len(failed_files)} of {total} clean modified/failed: {details}")

def test_evil_corpus():
    evil_files = [
        os.path.join(EVIL_CORPUS_DIR, f) 
        for f in os.listdir(EVIL_CORPUS_DIR) 
        if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))
    ]

    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    total = len(evil_files)

    for f in evil_files:
        out_file = "/tmp/out_evil.json"
        if os.path.exists(out_file):
            os.remove(out_file)

        result = subprocess.run([COMPILED_BIN, f, out_file], capture_output=True)

        bypassed = False
        reason = []
        if result.returncode == 0:
            bypassed = True
            reason.append("Exited with 0")

        if os.path.exists(out_file):
            bypassed = True
            reason.append("Output file created")

        if bypassed:
            failed_files.append((os.path.basename(f), " and ".join(reason)))

    if failed_files:
        details = ", ".join([f"{name} ({reason})" for name, reason in failed_files])
        pytest.fail(f"{len(failed_files)} of {total} evil bypassed: {details}")