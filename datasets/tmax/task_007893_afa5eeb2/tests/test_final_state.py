# test_final_state.py

import os
import struct
import pytest

def test_extract_c_exists():
    assert os.path.exists('/home/user/extract.c'), "The C source file /home/user/extract.c is missing."
    assert os.path.isfile('/home/user/extract.c'), "/home/user/extract.c is not a file."

def test_extract_executable_exists():
    assert os.path.exists('/home/user/extract'), "The executable /home/user/extract is missing."
    assert os.path.isfile('/home/user/extract'), "/home/user/extract is not a file."
    assert os.access('/home/user/extract', os.X_OK), "The file /home/user/extract is not executable."

def test_successful_amounts_csv():
    csv_path = '/home/user/successful_amounts.csv'
    dat_path = '/home/user/transactions.dat'

    assert os.path.exists(csv_path), f"The output file {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    # Derive expected output from the binary file
    assert os.path.exists(dat_path), f"The input file {dat_path} is missing."

    expected_rows = []
    with open(dat_path, 'rb') as f:
        while True:
            chunk = f.read(25)
            if not chunk:
                break
            if len(chunk) < 25:
                break

            tid, user, amount, status = struct.unpack('<I16sfB', chunk)
            if status == 1:
                expected_rows.append((tid, amount))

    expected_rows.sort(key=lambda x: x[0])

    expected_csv_lines = ["id,amount\n"]
    for tid, amount in expected_rows:
        expected_csv_lines.append(f"{tid},{amount:.2f}\n")

    expected_content = "".join(expected_csv_lines)

    with open(csv_path, 'r') as f:
        actual_content = f.read()

    # Normalize line endings
    actual_content = actual_content.replace('\r\n', '\n').strip() + '\n'
    expected_content = expected_content.replace('\r\n', '\n').strip() + '\n'

    assert actual_content == expected_content, f"The contents of {csv_path} do not match the expected output."