apt-get update && apt-get install -y python3 python3-pip libsndfile1
    pip3 install pytest numpy scipy librosa

    # Create /app directory
    mkdir -p /app

    # Generate data
    cat << 'EOF' > /tmp/setup.py
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import os
import librosa
from scipy.stats import wasserstein_distance

os.makedirs('/app', exist_ok=True)

fs = 16000
duration = 3.0
t = np.arange(int(fs * duration)) / fs

# Generate target signal: noise bandpassed around 1000Hz (Gaussian-like profile)
np.random.seed(42)
noise = np.random.randn(len(t))
b_target, a_target = signal.butter(4, [800/(fs/2), 1200/(fs/2)], btype='band')
target = signal.lfilter(b_target, a_target, noise)

# Generate distractor 1: 3000Hz tone with harmonics
dist1 = 0.5 * np.sin(2 * np.pi * 3000 * t) + 0.2 * np.sin(2 * np.pi * 6000 * t)

# Generate distractor 2: Low freq rumble 200Hz
dist2 = 0.8 * np.sin(2 * np.pi * 200 * t)

# Mix signals
mixed = target + dist1 + dist2

# Add near-singular artifact (amplitude modulation on all signals that causes rank deficiency)
mod = 1 + 0.5 * np.sin(2 * np.pi * 2 * t)
mixed = mixed * mod

# Save mixed signal for the agent
mixed_int16 = np.int16(mixed / np.max(np.abs(mixed)) * 32767)
wav.write('/app/sensor_data.wav', fs, mixed_int16)

# Generate golden reference using the exact expected agent pipeline
y_mixed = mixed_int16.astype(np.float32) / 32768.0
D = librosa.stft(y_mixed, n_fft=1024, hop_length=256, window='hann')
mag = np.abs(D)
phase = np.exp(1.j * np.angle(D))

U, S, Vt = np.linalg.svd(mag, full_matrices=False)

freqs = librosa.fft_frequencies(sr=fs, n_fft=1024)
analytical = np.exp(-((freqs - 1000)**2) / (2 * 150**2))
analytical /= np.sum(analytical)

best_dist = float('inf')
best_idx = 0

for i in range(3):
    u_col = np.abs(U[:, i])
    u_norm = u_col / np.sum(u_col)

    dist = wasserstein_distance(freqs, freqs, u_norm, analytical)
    if dist < best_dist:
        best_dist = dist
        best_idx = i

mag_clean = np.outer(U[:, best_idx], Vt[best_idx, :]) * S[best_idx]
D_clean = mag_clean * phase
y_clean = librosa.istft(D_clean, hop_length=256, window='hann', length=len(y_mixed))

# Save hidden reference
y_clean_int16 = np.int16(y_clean / np.max(np.abs(y_clean)) * 32767)
wav.write('/app/.hidden_reference.wav', fs, y_clean_int16)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user