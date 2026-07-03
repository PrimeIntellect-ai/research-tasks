# test_final_state.py
import os

def test_libvm_compiled():
    lib_path = "/home/user/pipeline/src/libvm.so"
    assert os.path.isfile(lib_path), f"Expected compiled library at {lib_path} is missing. The CMake build may have failed."

def test_run_vm_script_exists():
    script_path = "/home/user/pipeline/run_vm.py"
    assert os.path.isfile(script_path), f"Expected Python script at {script_path} is missing."

def test_result_file_content():
    result_path = "/home/user/pipeline/result.txt"
    assert os.path.isfile(result_path), f"Expected result file at {result_path} is missing. Did the Python script run?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    # Calculate the expected result: sum of squares of [4, 7, 2]
    expected_value = sum(x * x for x in [4, 7, 2])

    assert content == str(expected_value), f"Expected result file to contain '{expected_value}', but found '{content}'."