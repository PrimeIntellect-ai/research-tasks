apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install --no-cache-dir pytest pandas numpy networkx gTTS

    mkdir -p /app
    useradd -m -s /bin/bash user || true

    # Generate audio instructions
    python3 -c "from gtts import gTTS; gTTS('Please use a damping factor of zero point eight five, and run the PageRank algorithm for exactly forty five iterations.').save('/app/schema_instructions.mp3')"
    ffmpeg -i /app/schema_instructions.mp3 -ar 16000 /app/schema_instructions.wav
    rm /app/schema_instructions.mp3

    # Generate graph data
    cat << 'EOF' > /tmp/generate_data.py
import networkx as nx
import pandas as pd
import numpy as np

# Generate a directed graph
G = nx.barabasi_albert_graph(10000, 5, seed=42).to_directed()
# Add some dangling nodes
for i in range(10000, 10050):
    G.add_edge(0, i)

edges = list(G.edges())
pd.DataFrame(edges).to_csv('/home/user/edges.csv', index=False, header=False)

# Compute ground truth PageRank
N = 10050
edges_df = pd.DataFrame(edges, columns=['source', 'target'])
out_degree = edges_df.groupby('source').size().reindex(range(N), fill_value=0).values
dangling = np.where(out_degree == 0)[0]

adj = [[] for _ in range(N)]
for _, row in edges_df.iterrows():
    adj[row['target']].append(row['source'])

pr = np.full(N, 1.0 / N)
d = 0.85
iterations = 45

for _ in range(iterations):
    new_pr = np.zeros(N)
    dangling_sum = np.sum(pr[dangling])

    for i in range(N):
        s = 0.0
        for j in adj[i]:
            s += pr[j] / out_degree[j]
        new_pr[i] = (1 - d) / N + d * s + d * dangling_sum / N

    pr = new_pr

df = pd.DataFrame({'node': range(N), 'pr': pr})
df.to_csv('/tmp/ground_truth_pagerank.csv', index=False, header=False, float_format='%.9f')
EOF

    python3 /tmp/generate_data.py

    chmod -R 777 /home/user
    chmod -R 777 /app
    chmod 666 /tmp/ground_truth_pagerank.csv