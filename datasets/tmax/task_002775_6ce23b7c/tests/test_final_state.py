# test_final_state.py
import os
import re
import pytest

PIPELINE_DIR = "/home/user/pipeline"
DATA_CSV = os.path.join(PIPELINE_DIR, "data.csv")
CLEANER_CPP = os.path.join(PIPELINE_DIR, "cleaner.cpp")
RUN_SCRIPT = os.path.join(PIPELINE_DIR, "run_pipeline.sh")
MODEL_PARAMS = os.path.join(PIPELINE_DIR, "model_params.txt")

def test_cleaner_cpp_fixed():
    assert os.path.isfile(CLEANER_CPP), f"File {CLEANER_CPP} does not exist."
    with open(CLEANER_CPP, "r") as f:
        content = f.read()

    # The bug was `int total_sum = 0;` which caused integer truncation/overflow.
    # It should be changed to a floating point type (double or float).
    assert "int total_sum" not in content, "The bug 'int total_sum' is still present in cleaner.cpp."
    assert "double total_sum" in content or "float total_sum" in content or "auto total_sum = 0.0" in content, \
        "total_sum must be declared as a floating-point type (e.g., double) in cleaner.cpp."

def test_run_script_fixed():
    assert os.path.isfile(RUN_SCRIPT), f"File {RUN_SCRIPT} does not exist."
    with open(RUN_SCRIPT, "r") as f:
        content = f.read()

    # The run script must export DATASET_PATH or pass it directly to the executable.
    assert "DATASET_PATH=" in content, "DATASET_PATH is not being set in run_pipeline.sh."
    assert "data.csv" in content, "The path to data.csv is not provided in run_pipeline.sh."

def test_model_params_output():
    assert os.path.isfile(MODEL_PARAMS), f"Output file {MODEL_PARAMS} was not generated."

    with open(MODEL_PARAMS, "r") as f:
        content = f.read().strip()

    assert content != "", f"File {MODEL_PARAMS} is empty. The pipeline might have failed silently."

    # Parse m and c values
    match = re.search(r"m=([0-9\.\-]+),c=([0-9\.\-]+)", content)
    assert match is not None, f"Could not parse 'm' and 'c' values from {MODEL_PARAMS}. Content: {content}"

    m_val = float(match.group(1))
    c_val = float(match.group(2))

    # The expected values based on the cleaned dataset are m=2.0 and c=0.0
    assert abs(m_val - 2.0) < 1e-5, f"Expected m to be approximately 2.0, but got {m_val}."
    assert abs(c_val - 0.0) < 1e-5, f"Expected c to be approximately 0.0, but got {c_val}."