# test_final_state.py

import os
import math

def test_libspectrum_compiled():
    """Test that libspectrum.so has been compiled."""
    so_path = '/home/user/sim_project/libspectrum.so'
    assert os.path.isfile(so_path), f"{so_path} was not compiled or is missing."

def test_singular_values_output():
    """Test that singular_values.txt exists and contains the correct values."""
    file_path = '/home/user/sim_project/singular_values.txt'
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, f"{file_path} is empty."

    values_str = content.split(',')
    assert len(values_str) == 3, f"Expected 3 comma-separated values, got {len(values_str)}: {content}"

    try:
        values = [float(v.strip()) for v in values_str]
    except ValueError:
        assert False, f"Could not parse values in {file_path} as floats. Content: {content}"

    expected_values = [93.7547, 36.1772, 8.4116]

    for i, (val, exp) in enumerate(zip(values, expected_values)):
        assert math.isclose(val, exp, abs_tol=0.005), f"Singular value {i+1} is {val}, expected approximately {exp}."