apt-get update && apt-get install -y python3 python3-pip redis-server
    pip3 install pytest flask redis pyyaml numpy scipy requests

    mkdir -p /home/user/workspace/pipeline

    cat << 'EOF' > /tmp/setup.py
import os
import json
import numpy as np

os.makedirs('/home/user/workspace/pipeline', exist_ok=True)

# Generate synthetic sequences and reference distribution
np.random.seed(42)
reference_dist = np.random.normal(0.5, 0.1, 64) # 4^3 = 64 k-mers for k=3
np.save('/home/user/workspace/pipeline/reference_dist.npy', reference_dist)

# Generate sequences
sequences = {
    "seq_1": "".join(np.random.choice(['A', 'C', 'G', 'T'], 200)),
    "seq_2": "".join(np.random.choice(['A', 'C', 'G', 'T'], 200)),
    "seq_target": "CGAT" + "ATGCGTACGTAGCTAGCTAG" + "".join(np.random.choice(['A', 'C', 'G', 'T'], 176))
}
with open('/home/user/workspace/pipeline/sequences.json', 'w') as f:
    json.dump(sequences, f)

# config.yaml
with open('/home/user/workspace/pipeline/config.yaml', 'w') as f:
    f.write("""
api_port: 8050
redis_host: localhost
redis_port: 6379
""")

# redis.conf
with open('/home/user/workspace/pipeline/redis.conf', 'w') as f:
    f.write("port 6380\ndaemonize yes\n")

# api.py
with open('/home/user/workspace/pipeline/api.py', 'w') as f:
    f.write("""
from flask import Flask, jsonify
import json
import yaml

app = Flask(__name__)

@app.route('/sequences')
def get_sequences():
    with open('sequences.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    app.run(port=config['api_port'])
""")

# fit_model.py
with open('/home/user/workspace/pipeline/fit_model.py', 'w') as f:
    f.write("""
import requests
import redis
import yaml
import numpy as np

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

r = redis.Redis(host=config['redis_host'], port=config['redis_port'])

# Fetch
seqs = requests.get(f"http://localhost:{config['api_port']}/sequences").json()

# Cache and build k-mer profiles (k=3)
profiles = []
kmers = [a+b+c for a in 'ACGT' for b in 'ACGT' for c in 'ACGT']
for seq_id, seq in seqs.items():
    r.set(seq_id, seq)
    profile = [seq.count(k) for k in kmers]
    profiles.append(profile)

profiles = np.array(profiles).T # 64 x 3
cov = np.cov(profiles)

# Model fitting step (fails here due to near-singular cov matrix)
L = np.linalg.cholesky(cov)
print("Cholesky decomposition successful.")
""")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user