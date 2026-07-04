# test_final_state.py

import os
import subprocess
import json
import stat
import pytest

HOME_DIR = "/home/user"
PROCESSOR_C = os.path.join(HOME_DIR, "processor.c")
MAKEFILE = os.path.join(HOME_DIR, "Makefile")
CI_PIPELINE = os.path.join(HOME_DIR, "ci_pipeline.sh")
RESULT_JSON = os.path.join(HOME_DIR, "result.json")
CI_STATUS = os.path.join(HOME_DIR, "ci_status.log")
PROCESSOR_BIN = os.path.join(HOME_DIR, "processor")

def test_files_exist():
    """Verify that all required files exist."""
    assert os.path.isfile(PROCESSOR_C), f"File {PROCESSOR_C} does not exist."
    assert os.path.isfile(MAKEFILE), f"File {MAKEFILE} does not exist."
    assert os.path.isfile(CI_PIPELINE), f"File {CI_PIPELINE} does not exist."
    assert os.path.isfile(RESULT_JSON), f"File {RESULT_JSON} does not exist."
    assert os.path.isfile(CI_STATUS), f"File {CI_STATUS} does not exist."

def test_ci_pipeline_executable():
    """Verify that the CI pipeline script is executable."""
    assert os.path.isfile(CI_PIPELINE), f"File {CI_PIPELINE} does not exist."
    st = os.stat(CI_PIPELINE)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {CI_PIPELINE} is not executable."

def test_makefile_links_math():
    """Verify that the Makefile links the math library (-lm)."""
    assert os.path.isfile(MAKEFILE), f"File {MAKEFILE} does not exist."
    with open(MAKEFILE, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not link the math library (-lm)."

def test_ci_status_success():
    """Verify that ci_status.log indicates success."""
    assert os.path.isfile(CI_STATUS), f"File {CI_STATUS} does not exist."
    with open(CI_STATUS, "r") as f:
        content = f.read().strip()
    assert "CI PIPELINE SUCCESS" in content, f"ci_status.log does not contain 'CI PIPELINE SUCCESS'. Found: {content}"

def test_result_json_content():
    """Verify that result.json contains the correct expected output."""
    assert os.path.isfile(RESULT_JSON), f"File {RESULT_JSON} does not exist."
    with open(RESULT_JSON, "r") as f:
        content = f.read().strip()

    expected_str = '{"top_id": "dev_gamma", "max_sqrt": 10.00}'
    assert expected_str in content, f"result.json does not match exactly. Expected '{expected_str}', found '{content}'"

def test_make_clean_and_build():
    """Verify that make clean removes the binary, and make builds it again."""
    assert os.path.isfile(MAKEFILE), f"File {MAKEFILE} does not exist."

    # Ensure we are in the correct directory
    os.chdir(HOME_DIR)

    # Run make clean
    result = subprocess.run(["make", "clean"], capture_output=True, text=True)
    assert result.returncode == 0, f"'make clean' failed with output: {result.stderr}"
    assert not os.path.exists(PROCESSOR_BIN), f"'make clean' did not remove {PROCESSOR_BIN}."

    # Run make
    result = subprocess.run(["make"], capture_output=True, text=True)
    assert result.returncode == 0, f"'make' failed with output: {result.stderr}"
    assert os.path.isfile(PROCESSOR_BIN), f"'make' did not create {PROCESSOR_BIN}."
    assert os.access(PROCESSOR_BIN, os.X_OK), f"{PROCESSOR_BIN} is not executable."