# test_final_state.py
import os
import re

def derive_expected_message():
    """
    Parses the C source to extract the firmware blob, parses the TLV,
    and runs the VM to derive the expected output string.
    """
    c_file_path = "/home/user/legacy/libfirmware.c"
    if not os.path.exists(c_file_path):
        # Fallback if the C file was somehow removed, though constraints say not to modify legacy
        return "Hello World!"

    with open(c_file_path, "r") as f:
        content = f.read()

    match = re.search(r'firmware_data\[\]\s*=\s*\{([^}]+)\}', content)
    if not match:
        return "Hello World!"

    hex_str = match.group(1)

    # Extract bytes, ignoring comments
    bytes_list = []
    for line in hex_str.split('\n'):
        line = line.split('//')[0]
        for token in line.split(','):
            token = token.strip()
            if not token:
                continue
            try:
                bytes_list.append(int(token, 16))
            except ValueError:
                pass

    # Parse TLV
    idx = 0
    payload = []
    while idx < len(bytes_list):
        if idx + 2 >= len(bytes_list):
            break
        t = bytes_list[idx]
        l = bytes_list[idx+1] | (bytes_list[idx+2] << 8)
        idx += 3
        v = bytes_list[idx:idx+l]
        idx += l
        if t == 0x02:
            payload = v
            break

    # Run VM
    acc = 0
    out = bytearray()
    pc = 0
    while pc < len(payload):
        op = payload[pc]
        pc += 1
        if op == 0x10:  # LOAD
            if pc >= len(payload): break
            acc = payload[pc]
            pc += 1
        elif op == 0x11:  # ADD
            if pc >= len(payload): break
            acc = (acc + payload[pc]) & 0xFF
            pc += 1
        elif op == 0x12:  # XOR
            if pc >= len(payload): break
            acc = acc ^ payload[pc]
            pc += 1
        elif op == 0x20:  # OUT
            out.append(acc)
        elif op == 0xFF:  # HALT
            break

    try:
        return out.decode('utf-8')
    except UnicodeDecodeError:
        return "Hello World!"

def test_decoded_message_exists():
    output_path = "/home/user/decoded_message.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_decoded_message_content():
    output_path = "/home/user/decoded_message.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    expected_message = derive_expected_message()

    with open(output_path, "r") as f:
        actual_message = f.read().strip()

    assert actual_message == expected_message, (
        f"The decoded message is incorrect.\n"
        f"Expected: {expected_message!r}\n"
        f"Actual:   {actual_message!r}"
    )