apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy

    mkdir -p /app
    cat << 'EOF' > /tmp/generate_audio.py
import numpy as np
from scipy.io import wavfile

fs = 8000
duration = 1.0
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

alpha = 500.0
beta = 2.0
gamma = 300.0

# Phase function: phi(t) = (alpha/beta)*(exp(beta*t) - 1) + gamma*t
phi = (alpha / beta) * (np.exp(beta * t) - 1) + gamma * t

# Signal: s(t) = sin(2*pi*phi(t)) + 0.5*randn(t)
np.random.seed(42)
s = np.sin(2 * np.pi * phi) + 0.5 * np.random.randn(len(t))

# Normalize to 16-bit PCM
s_norm = np.int16(s / np.max(np.abs(s)) * 32767)

wavfile.write('/app/signal.wav', fs, s_norm)
EOF
    python3 /tmp/generate_audio.py
    rm /tmp/generate_audio.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user