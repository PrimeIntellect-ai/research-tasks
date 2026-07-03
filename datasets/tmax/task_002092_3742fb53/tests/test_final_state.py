# test_final_state.py

import os
import re

def parse_version(v):
    return tuple(map(int, v.split('.')))

def compute_magic_number(ops_path):
    reg = 0
    with open(ops_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 3:
                continue
            ver, op, val_str = parts[0], parts[1], parts[2]
            val = int(val_str)

            if parse_version(ver) >= (2, 1, 0):
                if op == 'ADD':
                    reg = (reg + val) % (1 << 32)
                elif op == 'SUB':
                    reg = (reg - val) % (1 << 32)
                elif op == 'MUL':
                    reg = (reg * val) % (1 << 32)
                elif op == 'XOR':
                    reg = (reg ^ val) % (1 << 32)
                elif op == 'LSHIFT':
                    reg = (reg << val) % (1 << 32)
                elif op == 'RSHIFT':
                    reg = (reg >> val) % (1 << 32)
    return reg

def test_magic_rs_content():
    magic_path = '/home/user/project/magic.rs'
    assert os.path.isfile(magic_path), f"The file {magic_path} was not generated."

    ops_path = '/home/user/project/ops.txt'
    expected_magic_number = compute_magic_number(ops_path)

    with open(magic_path, 'r') as f:
        content = f.read().strip()

    expected_content = f"pub const MAGIC_NUMBER: u32 = {expected_magic_number};"
    assert content == expected_content, f"Content of {magic_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_executable_exists():
    exe_path = '/home/user/project/main'
    assert os.path.isfile(exe_path), f"The compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_output_txt_content():
    output_path = '/home/user/project/output.txt'
    assert os.path.isfile(output_path), f"The file {output_path} does not exist."

    ops_path = '/home/user/project/ops.txt'
    expected_magic_number = compute_magic_number(ops_path)

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected_output = f"The magic number is: {expected_magic_number}"
    assert content == expected_output, f"Content of {output_path} is incorrect. Expected '{expected_output}', got '{content}'."