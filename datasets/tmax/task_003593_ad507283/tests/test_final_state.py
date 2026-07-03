# test_final_state.py
import numpy as np
from scipy.io import wavfile
import os

def generate_truth():
    fs, source = wavfile.read('/app/pulse.wav')
    S = source.astype(np.float64) / np.max(np.abs(source))
    dt = 1.0 / fs
    T = len(S) * dt
    c = 343.0
    gamma = 15.0
    L = 10.0

    dx = c * dt / 0.9
    Nx = int(np.ceil(L / dx)) + 1
    dx = L / (Nx - 1)
    Nt = len(S)

    u = np.zeros(Nx)
    u_prev = np.zeros(Nx)
    u_next = np.zeros(Nx)

    rec_idx = int(round(5.0 / dx))
    received_truth = np.zeros(Nt)

    C2 = (c * dt / dx)**2
    term1 = 2.0 / (1.0 + gamma * dt / 2.0)
    term2 = (1.0 - gamma * dt / 2.0) / (1.0 + gamma * dt / 2.0)

    for n in range(Nt):
        # Vectorized update for interior points
        u_next[1:-1] = term1 * (u[1:-1] + C2 / 2.0 * (u[2:] - 2*u[1:-1] + u[:-2])) - term2 * u_prev[1:-1]

        # Boundaries
        u_next[0] = S[n]
        u_next[-1] = 0.0

        received_truth[n] = u_next[rec_idx]

        u_prev[:] = u[:]
        u[:] = u_next[:]

    received_truth = received_truth / np.max(np.abs(received_truth))
    truth_audio = (received_truth * 32767).astype(np.int16).astype(np.float32)
    return fs, truth_audio

def test_received_signal_mse():
    agent_file = '/home/user/received_signal.wav'
    assert os.path.exists(agent_file), f"Agent output {agent_file} not found."

    try:
        fs_agent, agent_audio = wavfile.read(agent_file)
        agent_audio = agent_audio.astype(np.float32)
    except Exception as e:
        raise AssertionError(f"Error reading agent audio {agent_file}: {e}")

    fs_truth, truth_audio = generate_truth()

    assert fs_agent == fs_truth, f"Sample rate mismatch: agent has {fs_agent}, expected {fs_truth}"

    if len(agent_audio) != len(truth_audio):
        min_len = min(len(agent_audio), len(truth_audio))
        agent_audio = agent_audio[:min_len]
        truth_audio = truth_audio[:min_len]

    mse = np.mean((agent_audio / 32767.0 - truth_audio / 32767.0)**2)
    assert mse <= 1e-4, f"MSE {mse} exceeds threshold 1e-4"