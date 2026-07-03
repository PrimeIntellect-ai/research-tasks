# test_final_state.py

import os
import subprocess
import pytest

HOME_DIR = "/home/user"
ETL_PROCESSOR_C = os.path.join(HOME_DIR, "etl_processor.c")
MAKEFILE = os.path.join(HOME_DIR, "Makefile")
TEST_PIPELINE = os.path.join(HOME_DIR, "test_pipeline.sh")
CLEAN_DATA = os.path.join(HOME_DIR, "clean_data.csv")
REJECTED_LOG = os.path.join(HOME_DIR, "rejected.log")
EXECUTABLE = os.path.join(HOME_DIR, "etl_processor")

def test_files_exist():
    assert os.path.isfile(ETL_PROCESSOR_C), f"Missing {ETL_PROCESSOR_C}"
    assert os.path.isfile(MAKEFILE), f"Missing {MAKEFILE}"
    assert os.path.isfile(TEST_PIPELINE), f"Missing {TEST_PIPELINE}"

def test_pipeline_script_executable():
    assert os.access(TEST_PIPELINE, os.X_OK), f"{TEST_PIPELINE} is not executable"

def test_pipeline_execution():
    # Run the test_pipeline.sh script
    result = subprocess.run(
        [TEST_PIPELINE],
        cwd=HOME_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"test_pipeline.sh failed with exit code {result.returncode}. stderr: {result.stderr}"
    assert "REPRODUCIBLE" in result.stdout, "test_pipeline.sh did not print 'REPRODUCIBLE'"

def test_data_outputs():
    # Ensure the files were generated
    assert os.path.isfile(CLEAN_DATA), f"Missing {CLEAN_DATA} after running pipeline"
    assert os.path.isfile(REJECTED_LOG), f"Missing {REJECTED_LOG} after running pipeline"

    expected_clean = [
        "1,ACTIVE,10.50",
        "4,INACTIVE,5.50",
        "6,ACTIVE,100.00"
    ]

    expected_rejected = [
        "-2,ACTIVE,15.0",
        "3,UNKNOWN,20.0",
        "invalid,ACTIVE,1.0",
        "5,ACTIVE,badfloat"
    ]

    with open(CLEAN_DATA, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    with open(REJECTED_LOG, "r") as f:
        rejected_lines = [line.strip() for line in f if line.strip()]

    assert clean_lines == expected_clean, f"clean_data.csv contents mismatch. Got: {clean_lines}"
    assert rejected_lines == expected_rejected, f"rejected.log contents mismatch. Got: {rejected_lines}"

def test_makefile_clean():
    # Run make clean
    result = subprocess.run(
        ["make", "clean"],
        cwd=HOME_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"make clean failed. stderr: {result.stderr}"

    # Check that files are removed
    assert not os.path.exists(CLEAN_DATA), f"make clean did not remove {CLEAN_DATA}"
    assert not os.path.exists(REJECTED_LOG), f"make clean did not remove {REJECTED_LOG}"
    assert not os.path.exists(EXECUTABLE), f"make clean did not remove {EXECUTABLE}"