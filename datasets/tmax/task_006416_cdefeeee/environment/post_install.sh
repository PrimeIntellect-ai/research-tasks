apt-get update && apt-get install -y python3 python3-pip curl build-essential cargo rustc
    pip3 install pytest numpy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import math
import json
import numpy as np

# Create directories
os.makedirs("/home/user/input", exist_ok=True)
os.makedirs("/home/user/output", exist_ok=True)

# Generate a synthetic protein sequence
sequence = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN"
hydrophobic_chars = set("ACFILMVWY")

with open("/home/user/input/sequence.fasta", "w") as f:
    f.write(">1CRN\n")
    f.write(sequence + "\n")

# Generate synthetic PDB CA coordinates (random walk-ish, but deterministic)
np.random.seed(42)
coords = []
current = np.array([0.0, 0.0, 0.0])
for i in range(len(sequence)):
    coords.append(current.copy())
    current += np.random.normal(0, 3.8, 3) # ~3.8A between CA atoms

with open("/home/user/input/structure.pdb", "w") as f:
    for i, coord in enumerate(coords):
        # Format as standard PDB ATOM line
        f.write(f"ATOM  {i+1:>5}  CA  ALA A{i+1:>4}    {coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}  1.00 20.00           C  \n")

# Calculate Ground Truth
# 1. FFT
seq_vals = np.array([1.0 if c in hydrophobic_chars else 0.0 for c in sequence])
padded_len = 2**math.ceil(math.log2(len(sequence)))
padded_seq = np.zeros(padded_len)
padded_seq[:len(sequence)] = seq_vals

fft_res = np.fft.fft(padded_seq)
mags = np.abs(fft_res)
mags[0] = -1 # Ignore DC component
peak_idx = np.argmax(mags[:padded_len//2 + 1]) # only consider positive frequencies
peak_freq = round(peak_idx / padded_len, 3)

# 2. Graph
hydro_indices = [i for i, c in enumerate(sequence) if c in hydrophobic_chars]
adj_list = {i: [] for i in hydro_indices}

for i in range(len(hydro_indices)):
    for j in range(i + 1, len(hydro_indices)):
        idx1, idx2 = hydro_indices[i], hydro_indices[j]
        dist = np.linalg.norm(coords[idx1] - coords[idx2])
        if dist < 7.0:
            adj_list[idx1].append(idx2)
            adj_list[idx2].append(idx1)

visited = set()
max_cluster = 0
for node in hydro_indices:
    if node not in visited:
        # BFS/DFS
        q = [node]
        cluster_size = 0
        while q:
            curr = q.pop(0)
            if curr not in visited:
                visited.add(curr)
                cluster_size += 1
                for neighbor in adj_list[curr]:
                    if neighbor not in visited:
                        q.append(neighbor)
        if cluster_size > max_cluster:
            max_cluster = cluster_size

truth = {
    "peak_frequency": float(peak_freq),
    "largest_hydrophobic_cluster": int(max_cluster)
}

with open("/tmp/expected.json", "w") as f:
    json.dump(truth, f)
EOF

    python3 /tmp/setup.py

    chmod -R 777 /home/user