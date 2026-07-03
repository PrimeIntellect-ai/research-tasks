# test_final_state.py

import os
import ctypes
import pytest

class Instruction(ctypes.Structure):
    _fields_ = [("opcode", ctypes.c_int),
                ("value", ctypes.c_int)]

def test_test_success_log():
    log_path = "/home/user/math_vm/test_success.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. Property tests may not have run or passed."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "PROPERTY_TESTS_PASSED", f"Log file content is incorrect. Expected 'PROPERTY_TESTS_PASSED', got '{content}'"

def test_buffer_overflow_fixed():
    lib_path = "/home/user/math_vm/libvm.so"
    assert os.path.exists(lib_path), f"Compiled library {lib_path} is missing."

    lib = ctypes.CDLL(lib_path)
    lib.execute_vm.argtypes = [ctypes.POINTER(Instruction), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib.execute_vm.restype = ctypes.c_int

    # The original buggy C code had a hardcoded stack size of 10.
    # We will execute 100 PUSH instructions followed by 99 ADD instructions.
    # If the buffer overflow is not fixed, this will likely segfault or corrupt memory.
    num_pushes = 100
    instructions = [(0, 1)] * num_pushes + [(1, 0)] * (num_pushes - 1)

    arr = (Instruction * len(instructions))()
    for i, (op, val) in enumerate(instructions):
        arr[i].opcode = op
        arr[i].value = val

    res = ctypes.c_int()
    status = lib.execute_vm(arr, len(instructions), ctypes.byref(res))

    assert status == 0, "VM execution failed unexpectedly."
    assert res.value == num_pushes, f"Expected result {num_pushes}, got {res.value}. VM logic might be broken."

def test_memory_leak_fixed_in_source():
    vm_c_path = "/home/user/math_vm/vm.c"
    assert os.path.exists(vm_c_path), f"Source file {vm_c_path} is missing."

    with open(vm_c_path, "r") as f:
        code = f.read()

    # The original code had 2 free() calls on error paths, but missed the success path.
    # A correct fix should either have more free() calls or refactor to a single exit point.
    # We check that there are at least 3 free() calls, or some equivalent logic.
    free_count = code.count("free(")
    assert free_count >= 3, "Memory leak on success path does not appear to be fixed. Expected at least 3 free() calls in vm.c."

    # Also check that the stack is dynamically sized based on count or reallocated.
    # The original was malloc(10 * sizeof(int)).
    assert "malloc(10" not in code.replace(" ", ""), "Stack size is still hardcoded to 10. Buffer overflow fix is incomplete."