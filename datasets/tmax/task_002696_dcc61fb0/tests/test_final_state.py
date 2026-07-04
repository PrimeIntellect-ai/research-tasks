# test_final_state.py
import os
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import pytest

def test_filtered_audio_mse():
    agent_output_path = '/home/user/filtered.wav'
    fixture_path = '/app/test_audio.wav'

    assert os.path.isfile(agent_output_path), f"Agent's output file is missing at {agent_output_path}"
    assert os.path.isfile(fixture_path), f"Audio fixture is missing at {fixture_path}"

    # Generate reference
    rate, data = wav.read(fixture_path)
    if data.dtype == np.int16:
        data = data.astype(np.float64) / 32768.0

    # Filter coefficients as defined in the task
    b = [0.0001, 0.0002, 0.0001]
    a = [1.0, -1.98, 0.9801]

    # Compute reference output
    ref_out = signal.lfilter(b, a, data)
    ref_out = np.clip(ref_out, -1.0, 1.0)
    ref_out_int16 = (ref_out * 32767).astype(np.int16)

    # Read agent output
    agent_rate, agent_data = wav.read(agent_output_path)

    assert agent_rate == rate, f"Agent output sample rate {agent_rate} does not match fixture rate {rate}"
    assert len(agent_data) == len(ref_out_int16), "Agent output length does not match reference length"

    # Calculate MSE on float normalized values
    mse_float = np.mean(((ref_out_int16.astype(np.float64) / 32768.0) - (agent_data.astype(np.float64) / 32768.0))**2)

    assert mse_float < 1e-5, f"MSE {mse_float} is not less than threshold 1e-5"