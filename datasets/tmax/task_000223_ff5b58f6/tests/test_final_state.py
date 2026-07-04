# test_final_state.py

import os
import re
import pytest

def test_validation_log():
    log_path = '/home/user/validation.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    match = re.match(r'^MAE:\s*([0-9]*\.?[0-9]+)$', content)
    assert match is not None, f"Log file content '{content}' does not match expected format 'MAE: <value>'."

    mae = float(match.group(1))
    assert 0.0 <= mae < 0.1, f"MAE value {mae} is not within the expected range [0.0, 0.1)."

def test_hdf5_data():
    h5_path = '/home/user/benchmark_data.h5'
    assert os.path.exists(h5_path), f"HDF5 file {h5_path} does not exist."

    try:
        import h5py
        import numpy as np
    except ImportError:
        pytest.fail("Required libraries h5py and numpy are not installed.")

    try:
        with h5py.File(h5_path, 'r') as f:
            assert 'signals' in f, "Dataset 'signals' not found in HDF5 file."
            assert 'peak_frequencies' in f, "Dataset 'peak_frequencies' not found in HDF5 file."

            signals = f['signals']
            peaks = f['peak_frequencies']

            assert signals.shape == (1000, 10000), f"Expected signals shape (1000, 10000), got {signals.shape}"
            assert peaks.shape == (1000,), f"Expected peak_frequencies shape (1000,), got {peaks.shape}"

            # Verify a few rows to ensure correctness without taking too long
            np.random.seed(42)
            indices_to_check = np.random.choice(1000, size=10, replace=False)

            freqs = np.fft.rfftfreq(10000, d=1/1000)

            for idx in indices_to_check:
                row = signals[idx]
                fft_mag = np.abs(np.fft.rfft(row))
                expected_peak = freqs[np.argmax(fft_mag)]
                actual_peak = peaks[idx]

                assert np.isclose(actual_peak, expected_peak, atol=0.01), \
                    f"Row {idx}: expected peak {expected_peak}, got {actual_peak}"

    except OSError:
        pytest.fail(f"File {h5_path} is not a valid HDF5 file.")