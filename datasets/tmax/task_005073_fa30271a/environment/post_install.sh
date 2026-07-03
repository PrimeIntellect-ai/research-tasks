apt-get update && apt-get install -y python3 python3-pip postgresql redis-server sudo
    pip3 install pytest psycopg2-binary networkx pandas redis scipy

    useradd -m -s /bin/bash user || true
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

    mkdir -p /app
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
sudo service postgresql start
sudo service redis-server start
sudo su - postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'postgres';\""
EOF
    chmod +x /app/start_services.sh

    # Allow password authentication for postgres
    sed -i 's/peer/md5/g' /etc/postgresql/*/main/pg_hba.conf
    sed -i 's/scram-sha-256/md5/g' /etc/postgresql/*/main/pg_hba.conf

    # Generate data and reference output
    cat << 'EOF' > /app/setup.py
import pandas as pd
import numpy as np
import networkx as nx
import os

np.random.seed(42)
num_edges = 5000
source_ids = np.random.randint(1, 100, num_edges)
target_ids = np.random.randint(1, 100, num_edges)
timestamps = np.random.randint(1600000000, 1610000000, num_edges)
weights = np.random.uniform(0.1, 10.0, num_edges)

df = pd.DataFrame({
    'source_id': source_ids,
    'target_id': target_ids,
    'timestamp': timestamps,
    'interaction_weight': weights
})

os.makedirs('/home/user/data', exist_ok=True)
df.to_csv('/home/user/data/interactions.csv', index=False)

df_sorted = df.sort_values(['source_id', 'interaction_weight', 'timestamp', 'target_id'],
                           ascending=[True, False, True, True])
top3 = df_sorted.groupby('source_id').head(3)

G = nx.DiGraph()
for _, row in top3.iterrows():
    G.add_edge(row['source_id'], row['target_id'], interaction_weight=row['interaction_weight'])

pr = nx.pagerank(G, alpha=0.85, weight='interaction_weight')
pr_df = pd.DataFrame(list(pr.items()), columns=['node_id', 'pagerank_score'])
pr_df = pr_df.sort_values(['pagerank_score', 'node_id'], ascending=[False, True]).head(20)

pr_df.to_csv('/app/reference_top_nodes.csv', index=False)
EOF

    python3 /app/setup.py

    chmod -R 777 /app
    chmod -R 777 /home/user