# test_final_state.py
import os
import numpy as np
from scipy.io import wavfile
import pytest

def test_audio_denoising_mse():
    agent_path = '/home/user/clean_squiggle.wav'
    gt_path = '/app/ground_truth/clean_squiggle.wav'

    assert os.path.isfile(agent_path), f"Agent audio file missing at {agent_path}"
    assert os.path.isfile(gt_path), f"Ground truth audio file missing at {gt_path}"

    fs1, agent_audio = wavfile.read(agent_path)
    fs2, gt_audio = wavfile.read(gt_path)

    assert fs1 == fs2, f"Sample rate mismatch: agent {fs1}, gt {fs2}"
    assert len(agent_audio) == len(gt_audio), f"Audio length mismatch: agent {len(agent_audio)}, gt {len(gt_audio)}"

    mse = np.mean((agent_audio.astype(float) - gt_audio.astype(float))**2)
    assert mse < 5.0, f"MSE {mse:.4f} exceeds threshold of 5.0. The denoised audio is not accurate enough."

def test_alignment_position():
    pos_path = '/home/user/alignment_pos.txt'
    assert os.path.isfile(pos_path), f"Alignment position file missing at {pos_path}"

    with open(pos_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Alignment position file does not contain a valid integer: '{content}'"
    pos = int(content)
    assert pos == 42, f"Expected alignment position 42, got {pos}"

def test_features_extracted():
    features_path = '/home/user/features.npy'
    assert os.path.isfile(features_path), f"Features file missing at {features_path}"

    try:
        features = np.load(features_path)
    except Exception as e:
        pytest.fail(f"Failed to load features.npy: {e}")

    assert features.ndim == 2, f"Expected 2D feature matrix, got {features.ndim}D"

def test_spectrogram_plot_exists():
    plot_path = '/home/user/spectrogram_plot.png'
    assert os.path.isfile(plot_path), f"Spectrogram plot missing at {plot_path}"
    assert os.path.getsize(plot_path) > 0, f"Spectrogram plot file is empty"