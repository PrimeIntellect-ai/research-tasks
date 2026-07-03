apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy networkx scipy

    mkdir -p /home/user

    cat << 'EOF' > /tmp/setup.py
import os
import json
import numpy as np
import networkx as nx

# Create workspace
os.makedirs('/home/user', exist_ok=True)

# 1. Generate deterministic graph
G = nx.barabasi_albert_graph(20, 2, seed=42)
nodes = [f"P{i:02d}" for i in range(20)]
mapping = {i: nodes[i] for i in range(20)}
G = nx.relabel_nodes(G, mapping)

with open('/home/user/network.csv', 'w') as f:
    for u, v in G.edges():
        f.write(f"{u},{v}\n")

# 2. Generate source vector
np.random.seed(42)
S_vals = np.random.randn(20)
S_vals = S_vals - np.mean(S_vals) # ensure sum to 0

with open('/home/user/source.csv', 'w') as f:
    for i, node in enumerate(sorted(nodes)):
        f.write(f"{node},{S_vals[i]}\n")

# 3. Compute ground truth mathematically
nodelist = sorted(nodes)
A = nx.to_numpy_array(G, nodelist=nodelist)
D = np.diag(np.sum(A, axis=1))
L = D - A

M = np.linalg.matrix_power(L - 2*np.eye(20), 2)
c = np.linalg.pinv(M) @ S_vals

top_indices = np.argsort(c)[::-1][:2]
top_node_1 = nodelist[top_indices[0]]
top_node_2 = nodelist[top_indices[1]]

# 4. Plant primer in FASTA
primer = "TGCAGTACTCGATG"
np.random.seed(100)
with open('/home/user/sequences.fasta', 'w') as f:
    for i, node in enumerate(nodelist):
        seq = "".join(np.random.choice(['A','C','G','T'], 60))
        if i in top_indices:
            pos = np.random.randint(0, 40)
            seq = seq[:pos] + primer + seq[pos+len(primer):]
        f.write(f">{node}\n{seq}\n")

# 5. Generate truth reference
truth = {
    "top_node_1": top_node_1,
    "top_node_1_c": round(float(c[top_indices[0]]), 5),
    "top_node_2": top_node_2,
    "top_node_2_c": round(float(c[top_indices[1]]), 5),
    "primer_lcs": primer
}

with open('/home/user/.truth.json', 'w') as f:
    json.dump(truth, f, indent=4)
EOF

    python3 /tmp/setup.py
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user