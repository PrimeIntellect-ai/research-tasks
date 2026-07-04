# test_final_state.py

import os
import numpy as np
import scipy.io.wavfile as wavfile

def test_recovered_audio_mse():
    """Evaluate the Mean Squared Error (MSE) of the recovered audio against the hidden clean signal."""
    output_path = '/home/user/recovered_sensor.wav'
    clean_path = '/tmp/hidden_clean.wav'

    assert os.path.isfile(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(clean_path), f"Hidden clean file missing: {clean_path}"

    sr_clean, clean = wavfile.read(clean_path)
    sr_test, test = wavfile.read(output_path)

    # Ensure same length for comparison
    min_len = min(len(clean), len(test))
    clean_trimmed = clean[:min_len]
    test_trimmed = test[:min_len]

    mse = np.mean((clean_trimmed - test_trimmed) ** 2)
    threshold = 0.15

    assert mse <= threshold, f"MSE {mse:.4f} exceeds threshold {threshold}. Denoising was insufficient or incorrect."