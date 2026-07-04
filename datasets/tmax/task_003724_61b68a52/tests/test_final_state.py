# test_final_state.py
import os
import numpy as np
import scipy.io.wavfile as wavfile
import pytest

def compute_reference_correlation(audio_path):
    rate, data = wavfile.read(audio_path)
    if data.ndim > 1:
        data = data[:, 0]

    samples_per_chunk = 16000
    samples_per_window = 1600

    num_chunks = len(data) // samples_per_chunk
    features = []

    for i in range(num_chunks):
        chunk = data[i*samples_per_chunk : (i+1)*samples_per_chunk]
        chunk_features = []
        for j in range(10):
            window = chunk[j*samples_per_window : (j+1)*samples_per_window]
            mav = np.mean(np.abs(window.astype(float)))
            chunk_features.append(mav)
        features.append(chunk_features)

    features = np.array(features)
    corr_matrix = np.corrcoef(features)
    return corr_matrix

def test_correlation_matrix_mae():
    agent_file = '/home/user/artifacts/correlation.csv'
    assert os.path.exists(agent_file), f"Agent file not found: {agent_file}"

    try:
        agent_matrix = np.loadtxt(agent_file, delimiter=',')
    except Exception as e:
        pytest.fail(f"Failed to load {agent_file} as CSV: {e}")

    ref_matrix = compute_reference_correlation('/app/experiment_audio.wav')

    assert agent_matrix.shape == ref_matrix.shape, f"Shape mismatch: agent {agent_matrix.shape} != ref {ref_matrix.shape}"

    mae = np.mean(np.abs(ref_matrix - agent_matrix))
    assert mae <= 0.001, f"MAE {mae} exceeds threshold 0.001"

def test_similar_txt():
    similar_file = '/home/user/artifacts/similar.txt'
    assert os.path.exists(similar_file), f"Agent file not found: {similar_file}"

    ref_matrix = compute_reference_correlation('/app/experiment_audio.wav')

    # Get top 3 similar to chunk_00
    corr_with_00 = ref_matrix[0, 1:]

    # Sort by correlation descending, then index ascending (which is default argsort behavior on negated values)
    # Actually, we need to sort by correlation descending, and tie-break by index ascending.
    # We can use a structured array or just sort tuples.
    corrs = [(-corr_with_00[i], i + 1) for i in range(len(corr_with_00))]
    corrs.sort()
    expected_indices = [x[1] for x in corrs[:3]]

    with open(similar_file, 'r') as f:
        content = f.read().strip()

    assert content, "similar.txt is empty"
    try:
        agent_indices = [int(x.strip()) for x in content.split(',')]
    except ValueError:
        pytest.fail(f"Could not parse similar.txt contents: {content}")

    assert agent_indices == expected_indices, f"Expected indices {expected_indices}, got {agent_indices}"