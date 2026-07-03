# test_final_state.py

import os
import sys

def test_success_log():
    log_path = "/home/user/workspace/success.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist. The test script might not have been run or failed."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "PASS", f"Expected success.log to contain exactly 'PASS', got '{content}'"

def test_data_processor_assertion():
    dp_path = "/home/user/workspace/data_processor.py"
    assert os.path.isfile(dp_path), f"Expected {dp_path} to exist."
    with open(dp_path, "r") as f:
        content = f.read()

    assert "assert isinstance(data, list)" in content, "The required assertion 'assert isinstance(data, list)' is missing from data_processor.py"

def test_test_perf_restored():
    test_perf_path = "/home/user/workspace/test_perf.py"
    assert os.path.isfile(test_perf_path), f"Expected {test_perf_path} to be restored from the trash."

def test_data_processor_functionality():
    sys.path.insert(0, "/home/user/workspace")
    try:
        from data_processor import get_unique_elements
    except ImportError as e:
        assert False, f"Could not import data_processor.py: {e}"
    except SyntaxError as e:
        assert False, f"Syntax error in data_processor.py: {e}"

    test_data = [1, 2, 2, 3, 1, 4, 4, 5]
    try:
        result = get_unique_elements(test_data)
    except AssertionError:
        assert False, "get_unique_elements raised an AssertionError with valid list input."
    except Exception as e:
        assert False, f"get_unique_elements raised an unexpected exception: {e}"

    assert sorted(result) == [1, 2, 3, 4, 5], f"get_unique_elements did not return the correct unique elements. Got: {result}"