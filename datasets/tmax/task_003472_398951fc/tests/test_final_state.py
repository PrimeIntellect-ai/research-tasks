# test_final_state.py

import os
import numpy as np
import scipy.io.wavfile as wav
import h5py
import pytest

def test_hdf5_output():
    h5_path = '/home/user/analysis.h5'
    assert os.path.isfile(h5_path), f"HDF5 file {h5_path} does not exist."

    try:
        with h5py.File(h5_path, 'r') as f:
            assert 'spectrogram' in f, "Missing 'spectrogram' dataset in HDF5."
            assert 'std_dev' in f, "Missing 'std_dev' dataset in HDF5."

            spec = f['spectrogram'][:]
            std = f['std_dev'][:]

            assert len(spec.shape) == 2, f"Spectrogram must be 2D, got shape {spec.shape}"
            assert len(std.shape) == 1, f"std_dev must be 1D, got shape {std.shape}"
    except Exception as e:
        pytest.fail(f"Failed to read or validate HDF5 file: {e}")

def test_audio_mse():
    ref_path = '/truth/clean_reference.wav'
    test_path = '/home/user/cleaned.wav'

    assert os.path.isfile(test_path), f"Cleaned audio file {test_path} does not exist."
    assert os.path.isfile(ref_path), f"Reference audio file {ref_path} does not exist."

    try:
        fs1, ref = wav.read(ref_path)
        fs2, test = wav.read(test_path)
    except Exception as e:
        pytest.fail(f"Failed to read audio files: {e}")

    assert fs1 == fs2, f"Sample rates do not match: reference {fs1}, test {fs2}"

    # Normalize lengths if slight padding differences from STFT
    min_len = min(len(ref), len(test))
    ref_norm = ref[:min_len].astype(np.float32) / 32768.0
    test_norm = test[:min_len].astype(np.float32) / 32768.0

    mse = np.mean((ref_norm - test_norm) ** 2)
    threshold = 0.05

    assert mse <= threshold, f"Audio MSE is {mse:.6f}, which exceeds the threshold of {threshold}"