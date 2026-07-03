apt-get update && apt-get install -y python3 python3-pip espeak ffmpeg
pip3 install pytest numpy jupyter

mkdir -p /app

# Generate dictation audio
espeak -w /tmp/dictation_raw.wav "Hey, for the new pairwise structural distance metric, set the match multiplier alpha to zero point five, and the mismatch multiplier beta to one point two. Thanks."
ffmpeg -i /tmp/dictation_raw.wav -ar 16000 /app/dictation.wav

# Create slow_metric.py
cat << 'EOF' > /app/slow_metric.py
import sys
import json
import math

def run():
    data = json.load(sys.stdin)
    seq = data['sequence']
    coords = data['coords']
    n = len(seq)

    alpha = 0.5
    beta = 1.2

    total = 0.0
    for i in range(n):
        for j in range(n):
            c1 = coords[i]
            c2 = coords[j]
            dist = math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)
            if seq[i] == seq[j]:
                total += dist * alpha
            else:
                total += dist * beta

    print(f"{total:.4f}")

if __name__ == "__main__":
    run()
EOF

# Create oracle_dist wrapper
cat << 'EOF' > /app/oracle_dist
#!/bin/bash
python3 /app/slow_metric.py
EOF
chmod +x /app/oracle_dist

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user