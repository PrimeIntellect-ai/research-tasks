# test_final_state.py

import pytest
import requests
import numpy as np
from scipy.io import wavfile
from scipy import stats

def get_expected_results():
    sample_rate, audio_data = wavfile.read('/app/dna_telemetry.wav')
    chunk_size = int(sample_rate * 0.5)
    tone_len = int(sample_rate * 0.4)

    sequence = ""
    mapping = {
        (697, 1336): 'A',
        (697, 1477): 'C',
        (770, 1209): 'G',
        (770, 1336): 'T'
    }

    num_symbols = len(audio_data) // chunk_size
    if len(audio_data) % chunk_size >= tone_len:
        num_symbols += 1

    for i in range(num_symbols):
        start = i * chunk_size
        end = start + tone_len
        chunk = audio_data[start:end]

        f = np.fft.fftfreq(len(chunk), 1/sample_rate)
        mag = np.abs(np.fft.fft(chunk))

        low_freqs = [697, 770, 852, 941]
        high_freqs = [1209, 1336, 1477, 1633]

        low_mags = [mag[np.argmin(np.abs(f - x))] for x in low_freqs]
        high_mags = [mag[np.argmin(np.abs(f - x))] for x in high_freqs]

        f1 = low_freqs[np.argmax(low_mags)]
        f2 = high_freqs[np.argmax(high_mags)]

        sequence += mapping[(f1, f2)]

    bases = ['A', 'C', 'G', 'T']
    counts = np.zeros((4, 4))
    for i in range(len(sequence)-1):
        counts[bases.index(sequence[i]), bases.index(sequence[i+1])] += 1

    P = np.zeros((4, 4))
    for i in range(4):
        s = np.sum(counts[i])
        if s > 0:
            P[i] = counts[i] / s
        else:
            P[i] = 0.25

    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigvals - 1.0))
    stat_dist = np.real(eigvecs[:, idx])
    stat_dist /= np.sum(stat_dist)
    stat_dict = {b: float(stat_dist[i]) for i, b in enumerate(bases)}

    obs = counts.flatten()
    exp = np.array([[np.sum(counts[i]) * 0.25]*4 for i in range(4)]).flatten()

    mask = exp > 0
    obs_filtered = obs[mask]
    exp_filtered = exp[mask]

    chi2_stat, p_value = stats.chisquare(f_obs=obs_filtered, f_exp=exp_filtered)

    return sequence, stat_dict, float(p_value)

def test_api_results():
    try:
        response = requests.get('http://127.0.0.1:8000/results', timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at http://127.0.0.1:8000/results: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "sequence" in data, "Missing 'sequence' in response"
    assert "stationary_distribution" in data, "Missing 'stationary_distribution' in response"
    assert "p_value" in data, "Missing 'p_value' in response"

    expected_sequence, expected_stat_dist, expected_p_value = get_expected_results()

    assert data["sequence"] == expected_sequence, f"Expected sequence {expected_sequence}, got {data['sequence']}"

    for base in ['A', 'C', 'G', 'T']:
        assert base in data["stationary_distribution"], f"Missing base {base} in stationary_distribution"
        assert np.isclose(data["stationary_distribution"][base], expected_stat_dist[base], atol=1e-3), \
            f"Expected stationary distribution for {base} to be {expected_stat_dist[base]:.4f}, got {data['stationary_distribution'][base]}"

    assert np.isclose(data["p_value"], expected_p_value, atol=1e-3), \
        f"Expected p_value to be {expected_p_value:.4f}, got {data['p_value']}"