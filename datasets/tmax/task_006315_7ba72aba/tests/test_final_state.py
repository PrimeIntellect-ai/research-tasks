# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/polyglot_project"
FIXES_PATCH = os.path.join(PROJECT_DIR, "fixes.patch")
ORCHESTRATOR_PY = os.path.join(PROJECT_DIR, "orchestrator.py")
SUCCESS_LOG = os.path.join(PROJECT_DIR, "success.log")
WORKER_BIN = os.path.join(PROJECT_DIR, "worker")
PARSER_BIN = os.path.join(PROJECT_DIR, "parser")

def test_fixes_patch_exists():
    assert os.path.isfile(FIXES_PATCH), f"Patch file {FIXES_PATCH} does not exist."

def test_orchestrator_exists():
    assert os.path.isfile(ORCHESTRATOR_PY), f"Orchestrator script {ORCHESTRATOR_PY} does not exist."

def test_success_log_content():
    assert os.path.isfile(SUCCESS_LOG), f"Success log {SUCCESS_LOG} does not exist."
    with open(SUCCESS_LOG, 'r') as f:
        content = f.read()
    assert "E2E TESTS PASSED" in content, f"{SUCCESS_LOG} does not contain 'E2E TESTS PASSED'. Found: {content}"

def test_worker_output():
    assert os.path.isfile(WORKER_BIN), f"Worker binary {WORKER_BIN} does not exist. Orchestrator may have failed to compile it."
    try:
        output = subprocess.check_output([WORKER_BIN], text=True).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Worker binary failed to run: {e}")
    assert output == "Sum: 15", f"Worker output was '{output}', expected 'Sum: 15'."

def test_parser_output():
    assert os.path.isfile(PARSER_BIN), f"Parser binary {PARSER_BIN} does not exist. Orchestrator may have failed to compile it."
    try:
        output = subprocess.check_output([PARSER_BIN], text=True).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Parser binary failed to run: {e}")

    expected_output = "Read: hello\nWrite: hello world"
    assert output == expected_output, f"Parser output was '{output}', expected '{expected_output}'."