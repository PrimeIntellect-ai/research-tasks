apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user/legacy
    cat << 'EOF' > /home/user/legacy/audio_graph_server.py
# Python 2 legacy script
import wave
import json

def process():
    pass
EOF

    mkdir -p /app
    python3 -c "
import wave, struct
with wave.open('/app/interview.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    for _ in range(16000):
        f.writeframes(struct.pack('<h', 0))
"

    cat << 'EOF' > /app/oracle_audio_graph
#!/usr/bin/env python3
import sys
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio')
    parser.add_argument('--graph')
    args = parser.parse_args()
    print("{}")

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/oracle_audio_graph

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user