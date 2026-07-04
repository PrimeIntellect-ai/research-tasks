# test_final_state.py

import os
import math

def test_vm_c_exists():
    vm_c_path = "/home/user/vm.c"
    assert os.path.exists(vm_c_path), f"Source file {vm_c_path} does not exist. You need to write the C code."
    assert os.path.isfile(vm_c_path), f"Path {vm_c_path} is not a file."

def test_vm_executable_exists():
    vm_path = "/home/user/vm"
    assert os.path.exists(vm_path), f"Executable {vm_path} does not exist. Did you compile the C code?"
    assert os.path.isfile(vm_path), f"Path {vm_path} is not a file."
    assert os.access(vm_path, os.X_OK), f"File {vm_path} is not executable."

def test_vm_output_correct():
    output_path = "/home/user/vm_output.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did you run the VM?"
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    with open(output_path, "r") as f:
        content = f.read()

    expected_output = f"{math.factorial(10)}\n"
    assert content == expected_output, f"Content of {output_path} is incorrect. Expected '{expected_output}', got '{content}'."