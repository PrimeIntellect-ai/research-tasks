apt-get update && apt-get install -y python3 python3-pip ffmpeg libsm6 libxext6
    pip3 install pytest networkx pandas opencv-python-headless

    mkdir -p /app/hidden
    mkdir -p /home/user

    # Generate a sample video
    ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=30 -pix_fmt yuv420p /app/traffic_video.mp4

    # Generate trajectories data
    cat << 'EOF' > /app/generate_data.py
import json
import random

random.seed(42)
with open('/app/trajectories.jsonl', 'w') as f:
    for i in range(5000):
        record = {
            "vehicle_id": i,
            "path": [random.randint(1, 50) for _ in range(random.randint(3, 8))],
            "speed": random.uniform(10, 80)
        }
        f.write(json.dumps(record) + '\n')
EOF
    python3 /app/generate_data.py

    # Create the inefficient query pipeline
    cat << 'EOF' > /home/user/query_pipeline.py
import json
import networkx as nx

def main():
    data = []
    with open('/app/trajectories.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))

    # Inefficient filtering
    filtered = []
    for d in data:
        # Simulate an O(N^2) operation that can be optimized
        matches = [x for x in data if x['vehicle_id'] == d['vehicle_id']]
        if matches and d['speed'] > 50:
            filtered.append(d)

    G = nx.Graph()
    for d in filtered:
        path = d['path']
        for i in range(len(path)-1):
            G.add_edge(path[i], path[i+1])

    centrality = nx.betweenness_centrality(G)
    print(json.dumps(centrality))

if __name__ == "__main__":
    main()
EOF

    cp /home/user/query_pipeline.py /app/hidden/query_pipeline_original.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app