# test_final_state.py

import os
import stat
import pytest
import numpy as np
import scipy.io.wavfile as wav

def test_build_and_test_script_exists_and_executable():
    path = "/home/user/build_and_test.sh"
    assert os.path.isfile(path), f"Missing script: {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {path}"

def test_release_executable_exists():
    path = "/home/user/audio_filter_release"
    assert os.path.isfile(path), f"Missing release executable: {path}"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Release binary is not executable: {path}"

def test_filtered_wav_exists():
    path = "/home/user/filtered.wav"
    assert os.path.isfile(path), f"Missing output file: {path}"

def test_filtered_wav_accuracy():
    input_path = "/app/test_speech.wav"
    output_path = "/home/user/filtered.wav"

    assert os.path.isfile(input_path), f"Missing input file: {input_path}"
    assert os.path.isfile(output_path), f"Missing output file: {output_path}"

    try:
        rate1, data1 = wav.read(input_path)
    except Exception as e:
        pytest.fail(f"Failed to read input wav: {e}")

    try:
        rate2, data2 = wav.read(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read output wav: {e}")

    assert rate1 == rate2, f"Sample rate mismatch: {rate1} != {rate2}"
    assert len(data1) == len(data2), f"Length mismatch: {len(data1)} != {len(data2)}"

    # Calculate golden reference
    data_padded = np.pad(data1, (2, 0), mode='constant')
    golden = (data_padded[:-2]/3.0 + data_padded[1:-1]/3.0 + data_padded[2:]/3.0).astype(np.int16)

    mse = np.mean((data2.astype(np.float32) - golden.astype(np.float32))**2)

    assert mse < 0.01, f"MSE too high: {mse} >= 0.01. Output audio does not match the 3-tap moving average filter."