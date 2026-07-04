# test_final_state.py
import os
import struct

def test_recovered_bin():
    """Verify that the recovered binary log is carved correctly."""
    path = "/home/user/recovered.bin"
    assert os.path.isfile(path), f"Missing file: {path}"

    # Reconstruct the expected binary log based on the setup
    log_magic = b'LOG\x00'
    rec1 = struct.pack('>HH', 0, 4) + b'JUNK'
    rec2 = struct.pack('>HH', 1, 22) + b'FLAG{R3C0V3R3D_P4RS3D}'
    terminator = b'\xff\xff\xff\xff'
    expected_binary_log = log_magic + rec1 + rec2 + terminator

    with open(path, 'rb') as f:
        data = f.read()

    assert data == expected_binary_log, f"The contents of {path} do not exactly match the expected carved binary log."

def test_flag_txt():
    """Verify that the flag was successfully extracted and saved."""
    path = "/home/user/flag.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{R3C0V3R3D_P4RS3D}"
    assert content == expected_flag, f"The contents of {path} are incorrect. Expected '{expected_flag}', got '{content}'."