# test_final_state.py

import os

def test_deploy_plan_content():
    """Check that deploy_plan.txt exists and contains the correct accepted services in order."""
    plan_path = "/home/user/release_manager/deploy_plan.txt"
    assert os.path.isfile(plan_path), f"{plan_path} does not exist."

    with open(plan_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["auth", "payment", "logging", "cache"]
    assert lines == expected_lines, f"deploy_plan.txt content is incorrect. Expected {expected_lines}, got {lines}."

def test_input_file_exists():
    """Check that input.b64 exists."""
    input_path = "/home/user/release_manager/input.b64"
    assert os.path.isfile(input_path), f"{input_path} does not exist."

def test_c_source_files_exist():
    """Check that the required C source files exist."""
    validator_c = "/home/user/release_manager/validator.c"
    test_validator_c = "/home/user/release_manager/test_validator.c"

    assert os.path.isfile(validator_c), f"{validator_c} does not exist."
    assert os.path.isfile(test_validator_c), f"{test_validator_c} does not exist."

def test_cjson_library_exists():
    """Check that cJSON library files exist in the lib directory."""
    cjson_c = "/home/user/release_manager/lib/cJSON.c"
    cjson_h = "/home/user/release_manager/lib/cJSON.h"

    assert os.path.isfile(cjson_c), f"{cjson_c} does not exist."
    assert os.path.isfile(cjson_h), f"{cjson_h} does not exist."

def test_test_results_log_exists():
    """Check that test_results.log exists."""
    log_path = "/home/user/release_manager/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."