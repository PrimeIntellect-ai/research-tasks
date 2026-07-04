apt-get update && apt-get install -y python3 python3-pip libsndfile1
    pip3 install pytest numpy scipy pandas librosa scikit-learn

    cat << 'EOF' > /tmp/setup.py
import numpy as np
import scipy.io.wavfile as wavfile
import pandas as pd
import os

os.makedirs('/app', exist_ok=True)

# Generate hidden clean signal (sine wave)
sr = 22050
t = np.linspace(0, 5, 5 * sr, endpoint=False)
clean_signal = np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 880 * t)

# Generate noisy signal
np.random.seed(42)
noise = np.random.normal(0, 0.8, clean_signal.shape)
noisy_signal = clean_signal + noise

# Save noisy signal to the fixture location
wavfile.write('/app/sensor_data.wav', sr, noisy_signal.astype(np.float32))

# Save metadata csv (missing some frame IDs to trigger pandas float conversion)
# STFT with n_fft=2048, hop_length=512 -> ~216 frames
frames = np.arange(216)
metadata_frames = np.random.choice(frames, size=150, replace=False)
df_meta = pd.DataFrame({'frame_id': metadata_frames, 'sensor_status': 'active'})
df_meta.to_csv('/app/frame_metadata.csv', index=False)

# Save hidden clean signal for verifier
wavfile.write('/tmp/hidden_clean.wav', sr, clean_signal.astype(np.float32))
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app