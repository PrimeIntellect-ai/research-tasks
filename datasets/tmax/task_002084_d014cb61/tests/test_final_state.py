# test_final_state.py

import os
import struct
import pytest

def test_libeval_so_exists_and_is_shared_object():
    lib_path = "/home/user/project/libeval.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not built or does not exist."

    with open(lib_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{lib_path} is not a valid ELF file."

        # Read e_type at offset 16
        f.seek(16)
        e_type = struct.unpack("<H", f.read(2))[0]
        # ET_DYN is 3 (Shared object file)
        assert e_type == 3, f"{lib_path} is not built as a shared object (missing -shared / -fPIC)."

def test_output_log_correct():
    data_path = "/home/user/project/data.txt"
    log_path = "/home/user/project/output.log"

    assert os.path.isfile(data_path), f"Data file {data_path} is missing."
    assert os.path.isfile(log_path), f"Output log {log_path} was not created."

    with open(data_path, "r") as f:
        data_lines = [line.strip() for line in f if line.strip()]

    expected_output = []
    for i, line in enumerate(data_lines, 1):
        parts = line.split()
        if len(parts) != 3:
            continue
        op, arg1_str, arg2_str = parts
        a = int(arg1_str)
        b = int(arg2_str)

        if op == "ADD":
            res = a + b
        elif op == "SUB":
            res = a - b
        elif op == "MUL":
            res = a * b
        elif op == "DIV":
            res = a // b if b != 0 else 0
        else:
            res = 0

        expected_output.append(f"Line {i}: {op} {a} {b} = {res}")

    with open(log_path, "r") as f:
        actual_output = [line.strip() for line in f if line.strip()]

    assert len(actual_output) == len(expected_output), (
        f"Expected {len(expected_output)} lines in output.log, but found {len(actual_output)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_output, expected_output), 1):
        assert actual == expected, f"Mismatch on line {i} of output.log.\nExpected: {expected}\nActual:   {actual}"