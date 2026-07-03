# test_final_state.py

import os
import subprocess
import pytest
import glob

PROJECT_DIR = "/home/user/project"
SRC_DIR = os.path.join(PROJECT_DIR, "src")
INCLUDE_DIR = os.path.join(PROJECT_DIR, "include")
MAKEFILE_PATH = os.path.join(PROJECT_DIR, "Makefile")
LIB_PATH = os.path.join(PROJECT_DIR, "libhelpers.so")
ROUTER_PATH = os.path.join(PROJECT_DIR, "router.sh")
CLEAN_CORPUS_DIR = "/tests/corpus/clean"
EVIL_CORPUS_DIR = "/tests/corpus/evil"
QUERY_ENGINE = "/app/bin/query_engine"

def test_c_files_moved_to_src():
    assert os.path.isdir(SRC_DIR), f"Directory {SRC_DIR} is missing"
    c_files = glob.glob(os.path.join(SRC_DIR, "*.c"))
    assert len(c_files) > 0, "No .c files found in src directory"
    assert os.path.isfile(os.path.join(SRC_DIR, "utils.c")), "utils.c was not moved to src/"
    old_c_files = glob.glob(os.path.join(PROJECT_DIR, "*.c"))
    assert len(old_c_files) == 0, ".c files still exist in the project root"

def test_h_files_moved_to_include():
    assert os.path.isdir(INCLUDE_DIR), f"Directory {INCLUDE_DIR} is missing"
    h_files = glob.glob(os.path.join(INCLUDE_DIR, "*.h"))
    assert len(h_files) > 0, "No .h files found in include directory"
    assert os.path.isfile(os.path.join(INCLUDE_DIR, "utils.h")), "utils.h was not moved to include/"
    old_h_files = glob.glob(os.path.join(PROJECT_DIR, "*.h"))
    assert len(old_h_files) == 0, ".h files still exist in the project root"

def test_makefile_builds_shared_library():
    # Clean first if it exists
    if os.path.exists(LIB_PATH):
        os.remove(LIB_PATH)

    # Run make
    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Make failed with error:\n{result.stderr}"

    assert os.path.isfile(LIB_PATH), f"Shared library {LIB_PATH} was not built by make"

    # Verify it is a shared object
    file_output = subprocess.run(["file", LIB_PATH], capture_output=True, text=True).stdout
    assert "shared object" in file_output, f"{LIB_PATH} is not a valid shared object"

def test_router_is_executable():
    assert os.path.isfile(ROUTER_PATH), f"Router script {ROUTER_PATH} is missing"
    assert os.access(ROUTER_PATH, os.X_OK), f"Router script {ROUTER_PATH} is not executable"

def test_router_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for fpath in clean_files:
        with open(fpath, "r") as f:
            payload = f.read()

        result = subprocess.run([ROUTER_PATH], input=payload, text=True, capture_output=True)
        lines = result.stdout.strip().split("\n")

        if len(lines) < 2 or lines[0].strip() != "HTTP/1.1 200 OK":
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_files)}")

def test_router_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for fpath in evil_files:
        with open(fpath, "r") as f:
            payload = f.read()

        result = subprocess.run([ROUTER_PATH], input=payload, text=True, capture_output=True)
        output = result.stdout.strip()

        if output != "HTTP/1.1 400 Bad Request":
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}")