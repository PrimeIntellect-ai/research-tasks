# test_final_state.py

import os
import numpy as np
import pytest

def test_sensor_output_exists():
    output_path = '/home/user/sensor_output.bin'
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did you run the tool?"

def test_sensor_output_size():
    output_path = '/home/user/sensor_output.bin'
    expected_path = '/home/user/expected_output.bin'

    assert os.path.isfile(output_path), "Output file is missing."
    assert os.path.isfile(expected_path), "Expected reference file is missing."

    output_size = os.path.getsize(output_path)
    expected_size = os.path.getsize(expected_path)

    assert output_size == expected_size, (
        f"Output file size is incorrect. Expected {expected_size} bytes (10,000 doubles), "
        f"but got {output_size} bytes."
    )

def test_sensor_output_mae():
    output_path = '/home/user/sensor_output.bin'
    expected_path = '/home/user/expected_output.bin'

    assert os.path.isfile(output_path), "Output file is missing."
    assert os.path.isfile(expected_path), "Expected reference file is missing."

    output = np.fromfile(output_path, dtype=np.float64)
    expected = np.fromfile(expected_path, dtype=np.float64)

    assert len(output) == len(expected), (
        f"Number of elements mismatch: output has {len(output)}, expected {len(expected)}."
    )

    mae = np.mean(np.abs(output - expected))
    threshold = 1e-10

    assert mae < threshold, (
        f"Precision loss detected! Mean Absolute Error (MAE) is {mae}, "
        f"which is >= the threshold of {threshold}. The C source code fix might be incomplete."
    )