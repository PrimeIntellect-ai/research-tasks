# test_final_state.py

import os
import json
import struct
import math

def test_result_json_exists_and_correct():
    result_path = "/home/user/output/result.json"
    assert os.path.isfile(result_path), f"Expected output file {result_path} is missing."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {result_path} does not contain valid JSON."

    assert "total_sensor2" in data, f"Key 'total_sensor2' missing from {result_path}."

    # Compute the expected sum from the binary file
    bin_path = "/home/user/data/batch_01.bin"
    assert os.path.isfile(bin_path), f"Binary file {bin_path} is missing."

    expected_sum = 0.0
    record_size = 20
    fmt = '<IIfd'

    with open(bin_path, 'rb') as f:
        while True:
            chunk = f.read(record_size)
            if not chunk:
                break
            if len(chunk) == record_size:
                record = struct.unpack(fmt, chunk)
                expected_sum += record[3]

    actual_sum = data["total_sensor2"]
    assert math.isclose(actual_sum, expected_sum, rel_tol=1e-5), \
        f"Expected total_sensor2 to be approximately {expected_sum}, but got {actual_sum}."

def test_makefile_fixed():
    makefile_path = "/home/user/app/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "exitt 1" not in content, "The deliberate typo 'exitt 1' is still present in the Makefile."