# test_final_state.py

import os
import struct
import pytest

PROJECT_DIR = "/home/user/project"
DATA_V1_PATH = os.path.join(PROJECT_DIR, "data_v1.bin")
DATA_V2_PATH = os.path.join(PROJECT_DIR, "data_v2.bin")

def test_data_v2_exists():
    assert os.path.isfile(DATA_V2_PATH), f"The output file {DATA_V2_PATH} does not exist. Did you run the migration tool?"

def test_data_v2_correctness():
    assert os.path.isfile(DATA_V1_PATH), f"The input file {DATA_V1_PATH} is missing."
    assert os.path.isfile(DATA_V2_PATH), f"The output file {DATA_V2_PATH} is missing."

    with open(DATA_V1_PATH, "rb") as f:
        v1_data = f.read()

    assert len(v1_data) % 16 == 0, "Input data_v1.bin is corrupted or has an invalid size."
    num_records = len(v1_data) // 16

    with open(DATA_V2_PATH, "rb") as f:
        v2_data = f.read()

    expected_v2_size = num_records * 17
    assert len(v2_data) == expected_v2_size, (
        f"Expected data_v2.bin to be exactly {expected_v2_size} bytes for {num_records} records "
        f"(17 bytes per record), but got {len(v2_data)} bytes. Check your struct packing and padding."
    )

    for i in range(num_records):
        v1_offset = i * 16
        v2_offset = i * 17

        v1_chunk = v1_data[v1_offset:v1_offset+16]
        v2_chunk = v2_data[v2_offset:v2_offset+17]

        v1_unpacked = struct.unpack('<IfQ', v1_chunk)
        try:
            v2_unpacked = struct.unpack('<IBfQ', v2_chunk)
        except struct.error:
            pytest.fail(f"Record {i+1}: Failed to unpack 17 bytes as <IBfQ. Data might be malformed.")

        assert v2_unpacked[0] == v1_unpacked[0], f"Record {i+1}: ID mismatch. Expected {v1_unpacked[0]}, got {v2_unpacked[0]}."
        assert v2_unpacked[1] == 1, f"Record {i+1}: Flags mismatch. Expected 1 (0x01), got {v2_unpacked[1]}."

        # Float comparison
        assert abs(v2_unpacked[2] - v1_unpacked[1]) < 0.0001, (
            f"Record {i+1}: Value mismatch. Expected approx {v1_unpacked[1]}, got {v2_unpacked[2]}."
        )

        assert v2_unpacked[3] == v1_unpacked[2], f"Record {i+1}: Timestamp mismatch. Expected {v1_unpacked[2]}, got {v2_unpacked[3]}."