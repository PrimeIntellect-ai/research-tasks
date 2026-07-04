# test_final_state.py

import os
import numpy as np
import scipy.io.wavfile as wav

def test_clean_telemetry_mse():
    test_path = '/home/user/clean_telemetry.wav'
    reference_path = '/opt/reference_clean_telemetry.wav'

    assert os.path.isfile(test_path), f"Output file {test_path} does not exist."
    assert os.path.isfile(reference_path), f"Reference file {reference_path} does not exist. (Environment issue)"

    rate_ref, data_ref = wav.read(reference_path)
    try:
        rate_test, data_test = wav.read(test_path)
    except Exception as e:
        assert False, f"Failed to read {test_path} as a WAV file: {e}"

    assert rate_ref == rate_test, f"Sample rates do not match. Expected {rate_ref}, got {rate_test}."
    assert len(data_ref) == len(data_test), f"Audio lengths do not match. Expected {len(data_ref)} samples, got {len(data_test)}."

    # Normalize to -1.0 to 1.0 for MSE calculation
    data_ref_norm = data_ref.astype(np.float64) / 32768.0
    data_test_norm = data_test.astype(np.float64) / 32768.0

    mse = np.mean((data_ref_norm - data_test_norm) ** 2)

    threshold = 0.001
    assert mse <= threshold, f"MSE {mse:.6f} exceeds the maximum allowed threshold of {threshold}."