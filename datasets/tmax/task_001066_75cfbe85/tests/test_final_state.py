# test_final_state.py

import os
import numpy as np
import pytest

def compute_reference():
    # We import librosa locally to ensure it uses the agent's installed version if needed
    try:
        import librosa
    except ImportError:
        pytest.fail("librosa is not installed. The task required using librosa.")

    audio_path = "/app/input_audio.wav"
    if not os.path.exists(audio_path):
        pytest.fail(f"Input audio file missing at {audio_path}")

    # Load audio
    y, sr = librosa.load(audio_path, sr=16000)

    # Extract features
    rms = librosa.feature.rms(y=y, frame_length=320, hop_length=320, center=False)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y, frame_length=320, hop_length=320, center=False)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=13, n_fft=320, hop_length=320, n_mels=40, center=False)

    # Stack features: [RMS, ZCR, MFCC_1..13] -> shape (15, n_frames)
    features = np.vstack([rms, zcr, mfcc])

    # Feature selection: top 4 variances
    variances = np.var(features, axis=1)
    top_4_idx = np.argsort(variances)[-4:][::-1]

    # Filtering
    median_rms = np.median(rms)
    valid_frames = features[:, rms > median_rms]

    # Bootstrapping
    np.random.seed(42)
    n_valid = valid_frames.shape[1]
    sampled_indices = np.random.choice(n_valid, size=10000, replace=True)
    bootstrapped = valid_frames[top_4_idx][:, sampled_indices]

    return np.mean(bootstrapped, axis=1)

def test_prepared_features():
    output_path = "/home/user/prepared_features.csv"
    assert os.path.isfile(output_path), f"Output file is missing at {output_path}"

    try:
        agent_data = np.loadtxt(output_path, delimiter=",")
    except Exception as e:
        pytest.fail(f"Failed to load {output_path} as CSV: {e}")

    assert agent_data.shape == (10000, 4), f"Shape mismatch: expected (10000, 4), got {agent_data.shape}"

    agent_means = np.mean(agent_data, axis=0)
    ref_means = compute_reference()

    # Sort both to ignore column order mistakes
    agent_means = np.sort(agent_means)
    ref_means = np.sort(ref_means)

    rel_errors = np.abs((agent_means - ref_means) / (ref_means + 1e-9))
    max_err = np.max(rel_errors)

    assert max_err <= 0.05, f"Maximum relative error of column means is too high: {max_err:.4f} > 0.05"