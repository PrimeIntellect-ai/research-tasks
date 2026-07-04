apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest gTTS PyJWT

    mkdir -p /app/corpus/clean
    mkdir -p /app/corpus/evil

    cat << 'EOF' > /tmp/gen_audio.py
from gtts import gTTS
import os

text = "For the next phase, we are bypassing the API gateway using two JWT techniques. First, we are sending tokens with the algorithm header set to 'none', 'None', or 'nOnE' to bypass signature validation. Second, we are exploiting the 'kid' parameter by doing directory traversal attacks like dot-dot-slash to point the key ID to '/dev/null'. Make sure all payloads use one of these two methods."
tts = gTTS(text)
tts.save("/app/redteam_briefing.mp3")
EOF
    python3 /tmp/gen_audio.py
    ffmpeg -i /app/redteam_briefing.mp3 /app/redteam_briefing.wav
    rm /app/redteam_briefing.mp3
    rm /tmp/gen_audio.py

    cat << 'EOF' > /tmp/gen_jwts.py
import json
import base64

def encode_jwt(header, payload):
    h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    return f"{h}.{p}.signature"

with open('/app/corpus/clean/token1.txt', 'w') as f:
    f.write(encode_jwt({"alg": "RS256", "kid": "key1"}, {"user": "admin"}))

with open('/app/corpus/evil/token1.txt', 'w') as f:
    f.write(encode_jwt({"alg": "none", "kid": "key1"}, {"user": "admin"}))

with open('/app/corpus/evil/token2.txt', 'w') as f:
    f.write(encode_jwt({"alg": "RS256", "kid": "../../../dev/null"}, {"user": "admin"}))
EOF
    python3 /tmp/gen_jwts.py
    rm /tmp/gen_jwts.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app