# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
MAKEFILE_PATH = os.path.join(WORKSPACE_DIR, "Makefile")
SCRIPT_PATH = os.path.join(WORKSPACE_DIR, "run_qa.sh")
MOCK_CONFIG_PATH = os.path.join(WORKSPACE_DIR, "mock_config.ini")
QA_REPORT_PATH = os.path.join(WORKSPACE_DIR, "qa_report.txt")
PROCESSOR_PATH = os.path.join(WORKSPACE_DIR, "processor")

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile {MAKEFILE_PATH} is missing."

    with open(MAKEFILE_PATH, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("processor:"):
            deps = line.strip().split(':')[1].split()
            assert "processor" not in deps, "Makefile still contains circular dependency for 'processor'."
        if line.startswith("src/main.o:"):
            deps = line.strip().split(':')[1].split()
            assert "src/main.o" not in deps, "Makefile still contains circular dependency for 'src/main.o'."

def test_run_qa_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_run_qa_script_execution():
    # Remove artifacts if they exist to ensure the script creates them
    for path in [MOCK_CONFIG_PATH, QA_REPORT_PATH, PROCESSOR_PATH]:
        if os.path.exists(path):
            os.remove(path)

    result = subprocess.run(
        [SCRIPT_PATH], 
        cwd=WORKSPACE_DIR, 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, (
        f"run_qa.sh failed with exit code {result.returncode}.\n"
        f"Stdout:\n{result.stdout}\n"
        f"Stderr:\n{result.stderr}"
    )

def test_mock_config_content():
    assert os.path.isfile(MOCK_CONFIG_PATH), f"Mock config {MOCK_CONFIG_PATH} was not created."
    with open(MOCK_CONFIG_PATH, "r") as f:
        content = f.read()
    assert content == "MULTIPLIER=5\n", f"Mock config content is incorrect. Got: {repr(content)}"

def test_qa_report_content():
    assert os.path.isfile(QA_REPORT_PATH), f"QA report {QA_REPORT_PATH} was not created."
    expected_content = (
        "BUILD: SUCCESS\n"
        "MOCK: CREATED\n"
        "PROPERTY_TESTS: 10/10 PASSED\n"
        "BENCHMARK: 5 RUNS COMPLETED"
    )
    with open(QA_REPORT_PATH, "r") as f:
        content = f.read().strip()
    assert content == expected_content, f"QA report content is incorrect. Got:\n{content}"

def test_processor_binary_built():
    assert os.path.isfile(PROCESSOR_PATH), f"Processor binary {PROCESSOR_PATH} was not built."
    assert os.access(PROCESSOR_PATH, os.X_OK), f"Processor binary {PROCESSOR_PATH} is not executable."