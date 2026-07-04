# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt

def test_clean_wav_exists():
    """Test that the agent generated the clean.wav file."""
    output_wav = "/home/user/clean.wav"
    assert os.path.exists(output_wav), f"The output file {output_wav} does not exist."
    assert os.path.isfile(output_wav), f"The path {output_wav} is not a file."

def test_mse_threshold():
    """Test that the MSE between the agent's clean.wav and the reference is within the threshold."""
    agent_wav = "/home/user/clean.wav"
    original_wav = "/app/suspicious.wav"

    assert os.path.exists(agent_wav), f"Agent output {agent_wav} is missing."
    assert os.path.exists(original_wav), f"Original audio {original_wav} is missing."

    # Create the reference
    try:
        rate, data = wavfile.read(original_wav)
    except Exception as e:
        assert False, f"Failed to read {original_wav}: {e}"

    if data.ndim > 1:
        data = data.mean(axis=1)

    nyq = 0.5 * rate
    normal_cutoff = 4000 / nyq
    b, a = butter(5, normal_cutoff, btype='low', analog=False)
    reference_data = filtfilt(b, a, data)

    max_val = np.max(np.abs(reference_data))
    if max_val > 0:
        reference_data = np.int16(reference_data / max_val * 32767)
    else:
        reference_data = np.int16(reference_data)

    # Read agent's output
    try:
        agent_rate, agent_data = wavfile.read(agent_wav)
    except Exception as e:
        assert False, f"Failed to read {agent_wav}: {e}"

    if agent_data.ndim > 1:
        agent_data = agent_data.mean(axis=1)

    # Ensure lengths match
    min_len = min(len(reference_data), len(agent_data))
    assert min_len > 0, "Audio data is empty."

    # Calculate MSE
    mse = np.mean((reference_data[:min_len].astype(np.float32) - agent_data[:min_len].astype(np.float32))**2)

    threshold = 100.0
    assert mse <= threshold, f"MSE is {mse:.4f}, which is greater than the threshold of {threshold}."