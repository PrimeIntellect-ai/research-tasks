apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy flask fastapi uvicorn requests

    mkdir -p /app

    cat << 'EOF' > /tmp/generate_audio.py
import numpy as np
from scipy.io import wavfile

# Generate DTMF audio for a specific sequence
sequence = "ACGCGTAACCGT"
mapping = {'A': '2', 'C': '3', 'G': '4', 'T': '5'}
dtmf_freqs = {
    '2': (697, 1336),
    '3': (697, 1477),
    '4': (770, 1209),
    '5': (770, 1336)
}

sample_rate = 8000
tone_duration = 0.4
silence_duration = 0.1
t_tone = np.linspace(0, tone_duration, int(sample_rate * tone_duration), endpoint=False)
t_silence = np.zeros(int(sample_rate * silence_duration))

audio = []
for base in sequence:
    f1, f2 = dtmf_freqs[mapping[base]]
    tone = np.sin(2 * np.pi * f1 * t_tone) + np.sin(2 * np.pi * f2 * t_tone)
    audio.extend(tone)
    audio.extend(t_silence)

audio_data = np.array(audio)
# normalize
if np.max(np.abs(audio_data)) > 0:
    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
else:
    audio_data = np.int16(audio_data)
wavfile.write('/app/dna_telemetry.wav', sample_rate, audio_data)
EOF

    python3 /tmp/generate_audio.py
    rm /tmp/generate_audio.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app