# test_final_state.py
import os
import subprocess
import re
import pytest

BIN_PATH = "/home/user/pipeline-parser/target/release/pipeline_parser"
PROJECT_DIR = "/home/user/pipeline-parser"
VALID_PIPELINE = "/home/user/pipelines/valid.pipeline"
CIRCULAR_PIPELINE = "/home/user/pipelines/circular.pipeline"

def test_binary_exists():
    assert os.path.isfile(BIN_PATH), f"Executable not found at {BIN_PATH}. Did you compile in release mode?"
    assert os.access(BIN_PATH, os.X_OK), f"File at {BIN_PATH} is not executable."

def test_valid_pipeline_output():
    result = subprocess.run([BIN_PATH, VALID_PIPELINE], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution failed for {VALID_PIPELINE}\nStderr: {result.stderr}"

    stdout = result.stdout
    assert "RESULT: SUCCESS" in stdout, "Missing or incorrect 'RESULT: SUCCESS' in output."
    assert "ORDER: build, lint, test, deploy" in stdout, "Missing or incorrect 'ORDER: build, lint, test, deploy' in output."
    assert re.search(r"PEAK_MEM:\s*\d+", stdout), "Missing or incorrect 'PEAK_MEM: <bytes>' format in output."

def test_circular_pipeline_output():
    result = subprocess.run([BIN_PATH, CIRCULAR_PIPELINE], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution failed for {CIRCULAR_PIPELINE}\nStderr: {result.stderr}"

    stdout = result.stdout
    assert "RESULT: ERROR" in stdout, "Missing or incorrect 'RESULT: ERROR' in output."
    assert "CYCLE: compile -> link -> test -> compile" in stdout, "Missing or incorrect 'CYCLE: compile -> link -> test -> compile' in output."
    assert re.search(r"PEAK_MEM:\s*\d+", stdout), "Missing or incorrect 'PEAK_MEM: <bytes>' format in output."

def test_cargo_tests_pass():
    assert os.path.isdir(PROJECT_DIR), f"Rust project directory missing at {PROJECT_DIR}"
    result = subprocess.run(["cargo", "test"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"'cargo test' failed in {PROJECT_DIR}.\nStdout: {result.stdout}\nStderr: {result.stderr}"