apt-get update && apt-get install -y python3 python3-pip g++ socat cron netcat curl
    pip3 install pytest numpy scipy

    mkdir -p /app

    # Generate clean and noisy audio files
    cat << 'EOF' > /tmp/gen_audio.py
import numpy as np
from scipy.io import wavfile

sample_rate = 44100
duration = 2.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
clean = 0.5 * np.sin(2 * np.pi * 440 * t)

# Add high frequency noise
np.random.seed(42)
noise = 0.2 * np.random.normal(size=len(t))
noisy = clean + noise

clean_int16 = np.int16(clean * 32767)
noisy_int16 = np.int16(noisy * 32767)

wavfile.write('/app/clean_reference.wav', sample_rate, clean_int16)
wavfile.write('/app/noisy_backup.wav', sample_rate, noisy_int16)
EOF
    python3 /tmp/gen_audio.py
    rm /tmp/gen_audio.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user