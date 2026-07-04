# test_final_state.py
import os
import subprocess
import json

def test_file_exists():
    """Check that the output HDF5 file was generated."""
    assert os.path.exists('/home/user/training_data.h5'), "/home/user/training_data.h5 does not exist. The Rust program may not have run successfully or saved the file to the correct location."

def test_hdf5_contents():
    """Check that the HDF5 file contains the correct dataset and values."""
    # We use a subprocess to read the HDF5 file using h5py, to avoid importing third-party libraries directly in the pytest environment.
    script = """
import sys
try:
    import h5py
except ImportError:
    print('{"error": "h5py not installed"}')
    sys.exit(0)
import json

try:
    with h5py.File('/home/user/training_data.h5', 'r') as f:
        if 'mean_times' not in f:
            print(json.dumps({"error": "Dataset 'mean_times' not found"}))
            sys.exit(0)

        data = f['mean_times'][:]
        print(json.dumps(data.tolist()))
except Exception as e:
    print(json.dumps({"error": str(e)}))
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to execute verification script: {result.stderr}"

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Failed to parse output from verification script: {result.stdout}"

    if isinstance(output, dict) and "error" in output:
        assert False, f"Error reading HDF5 file: {output['error']}"

    mean_times = output
    assert isinstance(mean_times, list), "Dataset 'mean_times' is not a list/array."
    assert len(mean_times) == 3, f"Expected 3 values in 'mean_times', got {len(mean_times)}."

    # Graph 2 is a star graph with 4 leaves.
    # Expected time is max of 4 geometric random variables with p=0.3
    # E[max(G1, G2, G3, G4)] where G_i ~ Geom(0.3) is approx 6.06
    val_g2 = mean_times[1]
    assert 5.5 <= val_g2 <= 6.5, f"Graph 2 mean time {val_g2} is out of expected range [5.5, 6.5]. Check your simulation logic."

    # Graph 3 is a line graph of 6 nodes. Distance is 5.
    # Sum of 5 Geometrics with p=0.3 -> Expected time = 5 / 0.3 = 16.666
    val_g3 = mean_times[2]
    assert 15.5 <= val_g3 <= 17.5, f"Graph 3 mean time {val_g3} is out of expected range [15.5, 17.5]. Check your simulation logic."