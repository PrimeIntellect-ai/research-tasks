# test_final_state.py

import os
import sys
import math
import pytest

def test_qa_project_directory_exists():
    assert os.path.isdir("/home/user/qa_project"), "Directory /home/user/qa_project does not exist."

def test_welford_implementation():
    welford_path = "/home/user/qa_project/welford.py"
    assert os.path.isfile(welford_path), f"File {welford_path} does not exist."

    sys.path.insert(0, "/home/user/qa_project")
    try:
        from welford import calculate_sample_variance
    except ImportError:
        pytest.fail("Could not import calculate_sample_variance from welford.py")

    # Test small
    assert math.isclose(calculate_sample_variance([1, 2, 3]), 1.0), "Variance calculation is incorrect for small numbers."

    # Test numerical stability
    large_offset = 1e9
    data = [large_offset + 1, large_offset + 2, large_offset + 3]
    assert math.isclose(calculate_sample_variance(data), 1.0), "Variance calculation is not numerically stable (did you use Welford's algorithm?)."

    # Test ValueError
    with pytest.raises(ValueError):
        calculate_sample_variance([1.0])

    sys.path.pop(0)

def test_test_welford_contains_hypothesis():
    test_file = "/home/user/qa_project/test_welford.py"
    assert os.path.isfile(test_file), f"File {test_file} does not exist."

    with open(test_file, "r") as f:
        content = f.read()
        assert "@given" in content, "test_welford.py does not contain '@given' decorator from hypothesis."

def test_run_pipeline_script():
    script_path = "/home/user/qa_project/run_pipeline.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_result_log():
    log_path = "/home/user/pipeline_result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "PIPELINE_SUCCESS", f"Expected PIPELINE_SUCCESS in {log_path}, got {content}"