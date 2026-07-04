apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest numpy networkx scikit-learn scipy

useradd -m -s /bin/bash user || true
mkdir -p /home/user

cat << 'EOF' > /tmp/generate_data.py
import os
import numpy as np
import networkx as nx

np.random.seed(42)
N = 50
V = 20

adj_matrices = []
diameters = []
for i in range(N):
    while True:
        G = nx.erdos_renyi_graph(V, 0.3)
        if nx.is_connected(G):
            break
    adj_matrices.append(nx.to_numpy_array(G))
    diameters.append(nx.diameter(G))

adj_matrices = np.array(adj_matrices)
frequencies = np.linspace(100, 1000, 1000)
signals = []

for d in diameters:
    true_peak = 50.0 * d + 200.0
    sig = np.exp(-0.5 * ((frequencies - true_peak) / 10.0)**2)
    sig += np.random.normal(0, 0.1, 1000)
    signals.append(sig)

signals = np.array(signals)

np.savez('/home/user/dataset.npz', adj_matrices=adj_matrices, signals=signals, frequencies=frequencies)
EOF

python3 /tmp/generate_data.py
rm /tmp/generate_data.py

chmod -R 777 /home/user