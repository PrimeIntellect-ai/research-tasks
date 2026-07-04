# test_final_state.py

import os
import json
import stat
import tarfile
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "ci_pipeline.sh")
GENERATOR_BIN = os.path.join(PROJECT_DIR, "generator")
PROCESSOR_BIN = os.path.join(PROJECT_DIR, "processor")
TARBALL_FILE = os.path.join(PROJECT_DIR, "release.tar.gz")
RESULT_FILE = os.path.join(PROJECT_DIR, "benchmark_result.json")

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_FILE), f"Script {SCRIPT_FILE} does not exist."
    st = os.stat(SCRIPT_FILE)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_FILE} is not executable."

def test_binaries_exist():
    assert os.path.isfile(GENERATOR_BIN), f"Binary {GENERATOR_BIN} was not built."
    assert os.path.isfile(PROCESSOR_BIN), f"Binary {PROCESSOR_BIN} was not built."

def test_generator_is_statically_linked():
    assert os.path.isfile(GENERATOR_BIN), "Generator binary missing."
    try:
        result = subprocess.run(
            ["ldd", GENERATOR_BIN], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        output = result.stdout
    except FileNotFoundError:
        pytest.fail("ldd command not found to verify static linking.")

    assert "not a dynamic executable" in output, \
        f"generator is not statically linked. ldd output: {output.strip()}"

def test_processor_is_statically_linked():
    assert os.path.isfile(PROCESSOR_BIN), "Processor binary missing."
    try:
        result = subprocess.run(
            ["ldd", PROCESSOR_BIN], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        output = result.stdout
    except FileNotFoundError:
        pytest.fail("ldd command not found to verify static linking.")

    assert "not a dynamic executable" in output, \
        f"processor is not statically linked. ldd output: {output.strip()}"

def test_release_tarball():
    assert os.path.isfile(TARBALL_FILE), f"Tarball {TARBALL_FILE} missing."
    try:
        with tarfile.open(TARBALL_FILE, "r:gz") as tar:
            names = tar.getnames()
            names_bases = [os.path.basename(n) for n in names]
            assert "generator" in names_bases, "generator binary not found in release.tar.gz"
            assert "processor" in names_bases, "processor binary not found in release.tar.gz"
    except tarfile.ReadError:
        pytest.fail(f"{TARBALL_FILE} is not a valid gzip-compressed tarball.")

def test_benchmark_result():
    assert os.path.isfile(RESULT_FILE), f"Benchmark result {RESULT_FILE} missing."
    with open(RESULT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_FILE} is not valid JSON.")

    assert "status" in data, "JSON missing 'status' key."
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"

    assert "average_ms" in data, "JSON missing 'average_ms' key."
    # The value can be parsed as an int or float depending on how it was formatted, 
    # but it must represent an integer conceptually.
    val = data["average_ms"]
    assert isinstance(val, int) or (isinstance(val, float) and val.is_integer()) or (isinstance(val, str) and val.isdigit()), \
        f"average_ms should be a valid integer, got {val}"