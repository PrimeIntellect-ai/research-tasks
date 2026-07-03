# test_final_state.py
import os
import wave
import struct
import numpy as np
import pandas as pd
import pytest

def test_experiment_results_mae():
    csv_path = "/home/user/artifacts/experiment_results.csv"
    wav_path = "/app/machine_sound.wav"

    assert os.path.exists(csv_path), f"The artifact file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"The path {csv_path} is not a file."

    # Compute ground truth
    assert os.path.exists(wav_path), f"The audio file {wav_path} is missing."
    with wave.open(wav_path, 'rb') as f:
        n_frames_audio = f.getnframes()
        audio_bytes = f.readframes(n_frames_audio)

    samples = struct.unpack(f'<{n_frames_audio}h', audio_bytes)
    frame_size = 1600
    n_frames = len(samples) // frame_size

    gt_probs = []
    p_A = 0.1
    p_I = 0.9

    for i in range(n_frames):
        frame_samples = samples[i*frame_size : (i+1)*frame_size]
        rms = np.sqrt(np.mean(np.square(frame_samples)))

        # Predict
        p_A_pred = p_A * 0.95 + p_I * 0.05
        p_I_pred = p_A * 0.05 + p_I * 0.95

        # Update
        lik_A = (1.0 / (1000 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((rms - 5000) / 1000)**2)
        lik_I = (1.0 / (200 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((rms - 500) / 200)**2)

        unnorm_A = p_A_pred * lik_A
        unnorm_I = p_I_pred * lik_I

        p_A = unnorm_A / (unnorm_A + unnorm_I)
        p_I = unnorm_I / (unnorm_A + unnorm_I)

        gt_probs.append(p_A)

    # Read agent output
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read CSV {csv_path}: {e}")

    assert len(df) == n_frames, f"Expected {n_frames} rows in CSV, got {len(df)}"
    assert 'prob_active' in df.columns, "CSV must have a header 'prob_active'"

    agent_probs = df['prob_active'].values
    mae = np.mean(np.abs(agent_probs - gt_probs))

    threshold = 0.01
    assert mae < threshold, f"MAE of prob_active is {mae}, which is not below the threshold of {threshold}"