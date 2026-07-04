# test_final_state.py

import os
import pytest

def test_output_log_exists_and_correct():
    output_path = "/home/user/pr_review/output.log"

    assert os.path.exists(output_path), f"Output file is missing: {output_path}. Did you run the emulator script?"
    assert os.path.isfile(output_path), f"Output path is not a file: {output_path}"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == "SUCCESS: 28", f"Output log contains incorrect state. Expected 'SUCCESS: 28', got '{content}'"

def test_vm_py_modifications():
    vm_path = "/home/user/pr_review/src/vm.py"
    assert os.path.exists(vm_path), f"File missing: {vm_path}"

    with open(vm_path, 'r') as f:
        content = f.read()

    # Check for ABI definitions
    assert "argtypes" in content and "restype" in content, "The ctypes ABI definitions (argtypes and restype) are still missing in vm.py."
    assert "c_double" in content, "The ctypes ABI definitions should use ctypes.c_double."