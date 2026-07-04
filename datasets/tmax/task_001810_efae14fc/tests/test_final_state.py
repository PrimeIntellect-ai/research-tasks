# test_final_state.py
import os
import h5py
import numpy as np

def test_hdf5_output_and_metric():
    output_path = '/home/user/analysis.h5'
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    try:
        with h5py.File(output_path, 'r') as f:
            assert 'dominant_frequency' in f, "Dataset 'dominant_frequency' missing in HDF5."
            assert 'time_series' in f, "Dataset 'time_series' missing in HDF5."

            freq = float(f['dominant_frequency'][...])
            time_series = f['time_series'][...]

            assert isinstance(time_series, np.ndarray), "'time_series' should be an array."
            assert time_series.ndim == 1, "'time_series' should be a 1D array."
    except Exception as e:
        raise AssertionError(f"Failed to read HDF5 file or missing datasets: {e}")

    truth = 5.34
    error = abs(freq - truth)
    assert error <= 0.05, f"Dominant frequency {freq:.4f} Hz is not within 0.05 Hz of truth {truth} Hz. Absolute error: {error:.4f}"