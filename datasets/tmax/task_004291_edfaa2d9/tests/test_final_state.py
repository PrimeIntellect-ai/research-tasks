# test_final_state.py
import os
import numpy as np
import scipy.io.wavfile as wav

def test_clean_training_data_exists():
    """Check that the agent generated the expected output file."""
    output_path = '/home/user/clean_training_data.wav'
    assert os.path.isfile(output_path), f"The expected output file {output_path} is missing."

def test_clean_training_data_mse():
    """Calculate the MSE between the agent's audio and the hidden reference, and assert it meets the threshold."""
    ref_path = '/app/.hidden_reference.wav'
    agent_path = '/home/user/clean_training_data.wav'

    assert os.path.isfile(ref_path), f"Hidden reference file {ref_path} is missing."
    assert os.path.isfile(agent_path), f"Agent output file {agent_path} is missing."

    fs_ref, ref_audio = wav.read(ref_path)
    fs_agent, agent_audio = wav.read(agent_path)

    assert fs_ref == fs_agent, f"Sample rate mismatch: expected {fs_ref} Hz, got {fs_agent} Hz."

    # Truncate to the minimum length in case of minor frame/padding differences
    min_len = min(len(ref_audio), len(agent_audio))
    ref_norm = ref_audio[:min_len].astype(float) / 32768.0
    agent_norm = agent_audio[:min_len].astype(float) / 32768.0

    # Account for potential global sign flip from SVD
    mse_positive = np.mean((ref_norm - agent_norm)**2)
    mse_negative = np.mean((ref_norm + agent_norm)**2)
    mse = min(mse_positive, mse_negative)

    threshold = 1e-6
    assert mse < threshold, f"Reconstructed audio MSE {mse} is not strictly less than the threshold {threshold}."