# test_final_state.py

import os

def compute_fec(data: bytes) -> int:
    fec = 0x12345678
    for b in data:
        fec ^= b
        fec = ((fec << 5) | (fec >> 27)) & 0xFFFFFFFF
    return fec

def encode_varint(value: int) -> bytes:
    res = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            res.append(byte | 0x80)
        else:
            res.append(byte)
            break
    return bytes(res)

def test_output_bin_exists_and_correct():
    output_path = "/home/user/workspace/output.bin"
    assert os.path.exists(output_path), f"File {output_path} does not exist. The Rust application likely did not run or failed to create the file."

    with open(output_path, "rb") as f:
        content = f.read()

    payload = b"INTEGRATION_TEST_DATA"
    fec_value = compute_fec(payload)

    # Protobuf encoding
    # Field 1: payload (tag = 1, wire_type = 2 for length-delimited) -> 1 << 3 | 2 = 0x0A
    field1_tag = bytes([0x0A])
    field1_len = encode_varint(len(payload))
    field1_data = payload

    # Field 2: fec (tag = 2, wire_type = 0 for varint) -> 2 << 3 | 0 = 0x10
    field2_tag = bytes([0x10])
    field2_data = encode_varint(fec_value)

    expected_bytes = field1_tag + field1_len + field1_data + field2_tag + field2_data

    assert content == expected_bytes, f"Contents of {output_path} are incorrect. Expected {expected_bytes.hex()}, got {content.hex()}."