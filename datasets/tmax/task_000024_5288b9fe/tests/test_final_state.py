# test_final_state.py

import os
import subprocess
import pytest
import numpy as np
from scipy.io import wavfile

def test_check_script_output():
    check_script_path = "/home/user/check.py"
    audio_file_path = "/app/test_audio.wav"

    assert os.path.isfile(check_script_path), f"Missing check script at {check_script_path}"
    assert os.path.isfile(audio_file_path), f"Missing audio file at {audio_file_path}"

    # Calculate ground truth
    sample_rate, data = wavfile.read(audio_file_path)

    if data.dtype == np.int16:
        data_float = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data_float = data.astype(np.float32) / 2147483648.0
    else:
        data_float = data.astype(np.float32)

    if data_float.ndim > 1:
        data_float = np.mean(data_float, axis=1)

    truth_value = np.mean(np.abs(data_float))

    # Run the check script
    result = subprocess.run(["python3", check_script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"check.py failed to run. Stderr: {result.stderr}"

    output_str = result.stdout.strip()
    try:
        output_val = float(output_str)
    except ValueError:
        pytest.fail(f"check.py output could not be parsed as a float. Output was: {output_str!r}")

    error = abs(output_val - truth_value)
    assert error <= 0.001, (
        f"Metric threshold failed: Absolute Error {error} > 0.001. "
        f"Output: {output_val}, Truth: {truth_value}"
    )