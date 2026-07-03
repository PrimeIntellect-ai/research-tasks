apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest gTTS

    mkdir -p /app
    mkdir -p /home/user

    # Create the TTS script and generate the audio file
    cat << 'EOF' > /app/gen_audio.py
from gtts import gTTS
import os

text = "Hey IT, this is DevOps. Our telemetry_parser.py is completely broken. First, the voltage floats are being cast to standard Python floats and rounded to 2 decimal places, we are losing microvolt precision. We need it strictly parsed as high-precision decimals or strings out to 6 places just like the old oracle. Second, when it hits a line without a status after the pipe character, it drops the line entirely instead of returning an empty status string. Finally, whoever wrote the 'skip_corrupted' function used recursion, so when we get a burst of static, the recursion depth exceeds the limit and the whole pipeline crashes. Please rewrite the error recovery to use a standard loop and make sure it behaves exactly like the oracle binary. Thanks."
tts = gTTS(text)
tts.save("/app/temp.mp3")
EOF
    python3 /app/gen_audio.py
    ffmpeg -i /app/temp.mp3 /app/ticket_recording.wav
    rm /app/temp.mp3 /app/gen_audio.py

    # Create the oracle parser
    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys
import re
import json

for line in sys.stdin:
    line = line.strip('\n')
    match = re.match(r'^\[(\d+\.\d+)\] ([A-Za-z0-9_]+): (\d+\.\d+) \| (.*)$', line)
    if match:
        ts, dev, vol, stat = match.groups()
        vol_fmt = "{:.6f}".format(float(vol))
        print(json.dumps({"timestamp": ts, "device": dev, "voltage": vol_fmt, "status": stat}))
    else:
        print(json.dumps({"error": "corrupted_frame"}))
EOF
    chmod +x /app/oracle_parser

    # Create the buggy script
    cat << 'EOF' > /home/user/telemetry_parser.py
import sys
import re
import json

def skip_corrupted(lines, index):
    if index >= len(lines):
        return index
    line = lines[index].strip('\n')
    match = re.match(r'^\[(\d+\.\d+)\] ([A-Za-z0-9_]+): (\d+\.\d+) \| (.+)$', line)
    if match:
        return index
    return skip_corrupted(lines, index + 1)

def main():
    lines = sys.stdin.readlines()
    idx = 0
    while idx < len(lines):
        idx = skip_corrupted(lines, idx)
        if idx >= len(lines):
            break
        line = lines[idx].strip('\n')
        match = re.match(r'^\[(\d+\.\d+)\] ([A-Za-z0-9_]+): (\d+\.\d+) \| (.+)$', line)
        if match:
            ts, dev, vol, stat = match.groups()
            print(json.dumps({
                "timestamp": ts,
                "device": dev,
                "voltage": str(round(float(vol), 2)),
                "status": stat
            }))
        idx += 1

if __name__ == "__main__":
    main()
EOF

    # Create the crash log
    cat << 'EOF' > /home/user/crash_trace.log
Traceback (most recent call last):
  File "/home/user/telemetry_parser.py", line 32, in <module>
    main()
  File "/home/user/telemetry_parser.py", line 18, in main
    idx = skip_corrupted(lines, idx)
  File "/home/user/telemetry_parser.py", line 12, in skip_corrupted
    return skip_corrupted(lines, index + 1)
  File "/home/user/telemetry_parser.py", line 12, in skip_corrupted
    return skip_corrupted(lines, index + 1)
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user