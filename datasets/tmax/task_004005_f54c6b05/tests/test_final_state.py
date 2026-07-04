# test_final_state.py
import os
import numpy as np
from scipy.io import wavfile

def test_recovered_wav_matches_original():
    original_path = '/app/suspicious_payload.wav'
    recovered_path = '/home/user/recovered.wav'

    assert os.path.isfile(original_path), f"Original file missing: {original_path}"
    assert os.path.isfile(recovered_path), f"Recovered file missing: {recovered_path}"

    try:
        sr1, data1 = wavfile.read(original_path)
    except Exception as e:
        assert False, f"Failed to read original wav file: {e}"

    try:
        sr2, data2 = wavfile.read(recovered_path)
    except Exception as e:
        assert False, f"Failed to read recovered wav file: {e}"

    assert sr1 == sr2, f"Sample rate mismatch: {sr1} != {sr2}"
    assert len(data1) == len(data2), f"Length mismatch: {len(data1)} != {len(data2)}"

    data1 = data1.astype(np.float64)
    data2 = data2.astype(np.float64)

    mse = np.mean((data1 - data2) ** 2)
    threshold = 0.0001

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}"