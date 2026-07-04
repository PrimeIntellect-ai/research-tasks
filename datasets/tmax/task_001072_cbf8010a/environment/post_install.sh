apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest setuptools

    # Create oracle
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/dinuc_oracle
#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    seq_id = ""
    seq = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith(">"):
            if not seq_id:
                seq_id = line[1:].split()[0]
        else:
            seq += line

    L = len(seq)
    if L < 2:
        print(f"[ID] {seq_id}")
        print("[MATRIX] 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        print("[CHI2] 0.0000")
        return

    nucs = ['A', 'C', 'G', 'T']
    counts = {n: seq.count(n) for n in nucs}

    matrix = []
    obs = {}
    for x in nucs:
        for y in nucs:
            obs[x+y] = 0

    for i in range(L - 1):
        di = seq[i:i+2]
        if di in obs:
            obs[di] += 1

    for x in nucs:
        for y in nucs:
            matrix.append(obs[x+y])

    chi2 = 0.0
    for x in nucs:
        for y in nucs:
            exp = (counts[x] * counts[y]) / (L - 1)
            if exp > 0:
                chi2 += ((obs[x+y] - exp)**2) / exp

    print(f"[ID] {seq_id}")
    print(f"[MATRIX] {','.join(map(str, matrix))}")
    print(f"[CHI2] {chi2:.4f}")

if __name__ == '__main__':
    main()
EOF
    chmod +x /opt/oracle/dinuc_oracle

    # Create vendored package
    mkdir -p /app/vendored/fastakit-0.1.0/fastakit

    cat << 'EOF' > /app/vendored/fastakit-0.1.0/setup.py
from setuptools import setup, find_packages
setup(
    name='fastakit',
    version='0.1.0',
    packages=find_packages(),
)
EOF

    cat << 'EOF' > /app/vendored/fastakit-0.1.0/fastakit/__init__.py
from .reader import read_fasta
EOF

    cat << 'EOF' > /app/vendored/fastakit-0.1.0/fastakit/reader.py
def read_fasta(filepath):
    seq_id = ""
    seq = ""
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip("A")
            if not line: continue
            if line.startswith(">"):
                if not seq_id:
                    seq_id = line[1:].strip()
            else:
                seq += line
    return seq_id, seq
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user