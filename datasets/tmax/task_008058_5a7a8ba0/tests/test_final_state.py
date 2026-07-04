# test_final_state.py
import os
import subprocess

def test_result_txt():
    result_path = "/home/user/math_feature/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. Did you save the result?"
    with open(result_path, "r") as f:
        content = f.read().strip()
    assert content == "25", f"Expected result.txt to contain '25', but got '{content}'."

def test_compilation():
    exe_path = "/home/user/math_feature/rpn_vm"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you fix the Makefile and run make?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_rpn_vm_correctness():
    exe_path = "/home/user/math_feature/rpn_vm"

    # Test division
    result_div = subprocess.run([exe_path, "10 2 /"], capture_output=True, text=True)
    assert result_div.returncode == 0, "Execution of rpn_vm failed for division test."
    assert result_div.stdout.strip() == "5", f"Expected '10 2 /' to yield 5, but got '{result_div.stdout.strip()}'. The division bug is not fixed correctly."

    # Test subtraction
    result_sub = subprocess.run([exe_path, "10 2 -"], capture_output=True, text=True)
    assert result_sub.returncode == 0, "Execution of rpn_vm failed for subtraction test."
    assert result_sub.stdout.strip() == "8", f"Expected '10 2 -' to yield 8, but got '{result_sub.stdout.strip()}'. The subtraction bug is not fixed correctly."