# test_final_state.py

import os
import json
import struct

def compute_expected_state():
    json_path = "/home/user/api_test.json"
    assert os.path.isfile(json_path), f"Missing {json_path}"

    with open(json_path, "r") as f:
        data = json.load(f)

    instructions = data.get("instructions", [])

    bytecode = bytearray()
    stack = []

    for instr in instructions:
        parts = instr.strip().split()
        op = parts[0]
        if op == "PUSH":
            val = int(parts[1])
            bytecode.append(0x01)
            bytecode.extend(struct.pack("<H", val))
            stack.append(val)
        elif op == "ADD":
            bytecode.append(0x02)
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif op == "SUB":
            bytecode.append(0x03)
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif op == "MUL":
            bytecode.append(0x04)
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)

    final_val = stack[-1] if stack else None
    return bytes(bytecode), final_val

def test_api_payload_bin():
    payload_path = "/home/user/api_payload.bin"
    assert os.path.isfile(payload_path), f"File {payload_path} is missing. Did the script run and create it?"

    expected_bytes, _ = compute_expected_state()

    with open(payload_path, "rb") as f:
        actual_bytes = f.read()

    assert actual_bytes == expected_bytes, f"Binary payload in {payload_path} does not match expected bytecode."

def test_final_state_txt():
    state_path = "/home/user/final_state.txt"
    assert os.path.isfile(state_path), f"File {state_path} is missing. Did the script run and create it?"

    _, expected_val = compute_expected_state()

    with open(state_path, "r") as f:
        actual_val_str = f.read().strip()

    assert actual_val_str == str(expected_val), f"Final state in {state_path} is '{actual_val_str}', expected '{expected_val}'."