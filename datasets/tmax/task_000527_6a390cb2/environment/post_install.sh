apt-get update && apt-get install -y python3 python3-pip imagemagick fonts-dejavu g++
    pip3 install pytest

    mkdir -p /app

    convert -size 800x200 xc:white -font DejaVu-Sans -pointsize 18 -fill black \
      -draw "text 10,30 'Encoding: Voss (A=1, others=0; C=1, others=0; etc). Sum the power spectra of all 4 channels.'" \
      -draw "text 10,60 'Artifact signature: Peak at period length exactly N=8 (frequency index k = L/8).'" \
      -draw "text 10,90 'Threshold: If Power at k=L/8 is > 5x the average power across all frequencies, REJECT.'" \
      /app/filter_specs.png

    cat << 'EOF' > /tmp/gen_data.py
import os
import random

random.seed(42)
bases = ['A', 'C', 'G', 'T']

def generate_clean(length=512):
    return ''.join(random.choices(bases, k=length))

def generate_artifact(length=512):
    # Create a strong period 8 signal by enforcing 'A' every 8 bases
    seq = list(generate_clean(length))
    for i in range(0, length, 8):
        seq[i] = 'A'
    return ''.join(seq)

def save_seqs(dir_path, n, generator):
    os.makedirs(dir_path, exist_ok=True)
    for i in range(n):
        with open(os.path.join(dir_path, f"seq_{i}.txt"), 'w') as f:
            f.write(generator())

save_seqs("/app/reads/clean", 100, generate_clean)
save_seqs("/app/reads/artifact", 100, generate_artifact)
save_seqs("/app/eval_reads/clean", 50, generate_clean)
save_seqs("/app/eval_reads/artifact", 50, generate_artifact)
EOF

    python3 /tmp/gen_data.py
    rm /tmp/gen_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app