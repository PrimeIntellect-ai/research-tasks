# test_final_state.py

import os
import subprocess
import pytest

def test_h5_file_exists():
    h5_path = "/home/user/gc_data.h5"
    assert os.path.isfile(h5_path), f"HDF5 file {h5_path} is missing."

def test_h5_dataset_metadata():
    h5_path = "/home/user/gc_data.h5"
    assert os.path.isfile(h5_path), f"HDF5 file {h5_path} is missing."

    # Use h5dump to get the header
    try:
        result = subprocess.run(
            ["h5dump", "-H", h5_path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"h5dump failed on {h5_path}: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("h5dump command not found. Ensure hdf5-tools is installed.")

    output = result.stdout
    assert 'DATASET "gc_distribution"' in output or 'DATASET "/gc_distribution"' in output, \
        "Dataset 'gc_distribution' not found in the HDF5 file."

    assert "DATASPACE  SIMPLE { ( 10000 ) / ( 10000 ) }" in output or "DATASPACE  SIMPLE { ( 10000 ) / ( H5S_UNLIMITED ) }" in output or "10000" in output, \
        "Dataset dimensions must be exactly 10000."

def test_summary_file_exists_and_content():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} is missing."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    # The canonical glibc result is 33.31, but we can accept a small range just in case.
    # However, the prompt specifically mentions 33.31.
    assert content.startswith("Mean GC:"), f"Summary file does not start with 'Mean GC:'. Found: {content}"

    try:
        val_str = content.split("Mean GC:")[1].strip()
        val = float(val_str)
        assert 33.00 <= val <= 34.00, f"Calculated mean {val} is outside the expected range (33.00 - 34.00)."
    except ValueError:
        pytest.fail(f"Could not parse the mean value from summary file content: {content}")