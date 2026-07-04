apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create directories
    mkdir -p /app/restored_data/raw/incidents/audio/
    mkdir -p /app/restored_data/raw/logs/

    # Create dummy logs
    echo "Incident 001: System alert triggered." > /app/restored_data/raw/logs/incident_001.log
    echo "System started normally." > /app/restored_data/raw/logs/sys.log

    # Generate a 10-second 16kHz 16-bit PCM WAV file
    python3 -c "
import wave
import math
import struct

sample_rate = 16000
duration = 10
num_samples = sample_rate * duration

with wave.open('/app/restored_data/raw/incidents/audio/alert_001.wav', 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    for i in range(num_samples):
        value = int(32767.0 * math.sin(2.0 * math.pi * 440.0 * i / sample_rate))
        data = struct.pack('<h', value)
        wf.writeframesraw(data)
"

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user