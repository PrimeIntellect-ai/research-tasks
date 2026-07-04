# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile

def calculate_peak_dbfs(filepath):
    samplerate, data = wavfile.read(filepath)
    # Convert to float
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0

    peak_amplitude = np.max(np.abs(data))
    if peak_amplitude == 0:
        return -float('inf')
    peak_dbfs = 20 * np.log10(peak_amplitude)
    return peak_dbfs

def test_output_wav_peak_dbfs():
    output_path = '/home/user/processed/output.wav'
    assert os.path.exists(output_path), f"Output file does not exist: {output_path}"

    actual_dbfs = calculate_peak_dbfs(output_path)
    target_dbfs = -3.0
    metric_value = abs(actual_dbfs - target_dbfs)

    assert metric_value <= 0.1, (
        f"Peak dBFS is {actual_dbfs:.2f}, expected {target_dbfs}. "
        f"Difference {metric_value:.2f} is greater than tolerance 0.1."
    )

def test_success_eml():
    eml_path = '/home/user/reports/success.eml'
    assert os.path.exists(eml_path), f"Success email file does not exist: {eml_path}"

    with open(eml_path, 'r') as f:
        content = f.read()

    assert 'Subject: Audio Processed' in content, "Success email does not contain 'Subject: Audio Processed'."

def test_virtual_fstab():
    fstab_path = '/home/user/virtual_fstab'
    assert os.path.exists(fstab_path), f"Virtual fstab file does not exist: {fstab_path}"

    with open(fstab_path, 'r') as f:
        content = f.read().strip()

    expected_line = 'none /home/user/reports tmpfs defaults 0 0'
    assert expected_line in content, f"Virtual fstab does not contain the expected line. Found: {content}"