# test_final_state.py

import os
import pstats
import pytest

def test_script_exists():
    """Verify that the simulation script exists."""
    script_path = "/home/user/simulate_and_profile.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_hdf5_file_exists_and_size():
    """Verify that the HDF5 results file exists and has a reasonable size."""
    h5_path = "/home/user/simulation_results.h5"
    assert os.path.exists(h5_path), f"HDF5 file {h5_path} is missing."
    assert os.path.isfile(h5_path), f"{h5_path} is not a file."
    # 4 datasets of 1,000,000 floats (8 bytes each) is ~32MB. 
    # Just check it's larger than 1MB to ensure it contains data.
    size_bytes = os.path.getsize(h5_path)
    assert size_bytes > 1_000_000, f"HDF5 file {h5_path} is too small ({size_bytes} bytes), datasets might be missing."

def test_validation_file():
    """Verify the validation output file contains a correct error value."""
    val_path = "/home/user/validation.txt"
    assert os.path.exists(val_path), f"Validation file {val_path} is missing."
    assert os.path.isfile(val_path), f"{val_path} is not a file."

    with open(val_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {val_path} could not be parsed as a float: {content}")

    assert abs(val) < 1e-4, f"Validation error {val} is greater than expected (should be close to 0.0)."

def test_profiling_file():
    """Verify the profiling output is a valid cProfile stats file."""
    prof_path = "/home/user/simulation.prof"
    assert os.path.exists(prof_path), f"Profiling file {prof_path} is missing."
    assert os.path.isfile(prof_path), f"{prof_path} is not a file."

    try:
        stats = pstats.Stats(prof_path)
    except Exception as e:
        pytest.fail(f"Could not parse {prof_path} as a pstats file: {e}")

    assert stats.total_calls > 0, f"Profiling file {prof_path} contains no function calls."