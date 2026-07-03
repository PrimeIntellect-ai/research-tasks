# test_final_state.py

import os
import re
import pytest

def test_integrate_c_fixed():
    path = "/home/user/sim/integrate.c"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check that the bug was fixed (dt * 0.5 instead of dt * 2.0)
    assert "dt * 2.0" not in content, "The bug 'dt * 2.0' is still present in integrate.c."
    assert "0.5" in content, "The multiplier was not changed to 0.5 (or similar logic) in integrate.c."

    # Check that MPI_Allreduce was added
    assert "MPI_Allreduce" in content, "MPI_Allreduce is missing from integrate.c."
    assert "MPI_MIN" in content, "MPI_MIN is missing from the MPI_Allreduce call in integrate.c."

def test_executable_exists():
    path = "/home/user/sim/integrate"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_hdf5_output_exists():
    path = "/home/user/sim/output.h5"
    assert os.path.isfile(path), f"HDF5 output file {path} is missing. Did you run the simulation?"

def test_result_txt_exists_and_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} is missing. Did you run h5dump?"

    with open(path, "r") as f:
        content = f.read()

    # Check that h5dump output format is present
    assert "HDF5" in content, f"{path} does not appear to contain h5dump output."
    assert "DATA {" in content, f"{path} does not contain dataset data."

    # Extract the values from the dataset
    # The dataset contains 4 double precision values.
    # The total integration time is 1.0, and val += dt * 0.5 at each step.
    # Total added value is 1.0 * 0.5 = 0.5.
    # Initial values are 1.0, 2.0, 3.0, 4.0.
    # Final expected values: 1.5, 2.5, 3.5, 4.5.

    expected_values = [1.5, 2.5, 3.5, 4.5]

    for val in expected_values:
        assert str(val) in content, f"Expected value {val} not found in {path}. The simulation logic or MPI execution might be incorrect."

    # Validate the number of elements dumped (should be 4 for 4 MPI processes)
    # A simple check is to find the data section and count the numbers.
    data_section = re.search(r'DATA\s*\{\s*(.*?)\s*\}', content, re.DOTALL)
    if data_section:
        data_str = data_section.group(1)
        # Find all floating point numbers in the data section
        numbers = re.findall(r'\d+\.\d+', data_str)
        if numbers:
            assert len(numbers) >= 4, f"Expected at least 4 values in the dataset, found {len(numbers)}."