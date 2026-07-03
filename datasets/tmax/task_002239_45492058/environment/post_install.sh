apt-get update && apt-get install -y python3 python3-pip g++ bc time espeak ffmpeg
    pip3 install pytest numpy

    # Create directories
    mkdir -p /app
    mkdir -p /home/user/data
    mkdir -p /home/user/output

    # Generate audio file
    espeak -w /app/instructions.wav "Please filter the sequences for the motif ACGTTGC and use a k-mer size of four."

    # Generate FASTA file
    python3 -c '
import random
random.seed(42)
bases = ["A", "C", "G", "T"]
motif = "ACGTTGC"
with open("/home/user/data/sequences.fasta", "w") as f:
    for i in range(500):
        seq = "".join(random.choices(bases, k=1000))
        if i < 50:
            pos = random.randint(0, 1000 - len(motif))
            seq = seq[:pos] + motif + seq[pos+len(motif):]
        f.write(f">seq_{i}\n{seq}\n")
'

    # Create user
    useradd -m -s /bin/bash user || true

    # Set permissions
    chmod -R 777 /home/user
    chmod -R 777 /app