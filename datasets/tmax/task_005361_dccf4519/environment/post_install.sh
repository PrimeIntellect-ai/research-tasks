apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest networkx numpy scipy

mkdir -p /app
cat << 'EOF' > /app/graph_oracle
#!/usr/bin/env python3
import sys
import time
import networkx as nx

if len(sys.argv) != 3:
    print("Usage: graph_oracle <input_edgelist.txt> <output_scores.txt>")
    sys.exit(1)

infile = sys.argv[1]
outfile = sys.argv[2]

G = nx.DiGraph()
with open(infile, 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            u, v = int(parts[0]), int(parts[1])
            G.add_edge(u, v)

# Artificial delay to simulate poor performance
time.sleep(5)

pr = nx.pagerank(G, alpha=0.75, max_iter=100, tol=1e-06)

with open(outfile, 'w') as f:
    for node in sorted(pr.keys()):
        f.write(f"{node}\t{pr[node]:.6f}\n")
EOF
chmod +x /app/graph_oracle

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user