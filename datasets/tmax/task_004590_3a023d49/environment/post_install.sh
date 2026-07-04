apt-get update && apt-get install -y python3 python3-pip ffmpeg zbar-tools
    pip3 install pytest qrcode pillow

    mkdir -p /app

    # Create oracle script
    cat << 'EOF' > /app/oracle_etl_graph.py
import sys
import json
from collections import defaultdict

def main():
    graph = defaultdict(list)
    graph["ROOT"].extend(["DB_1", "DB_2"])
    graph["DB_1"].extend(["Collection_A", "Collection_B"])
    graph["DB_2"].extend(["Collection_C"])

    try:
        input_data = sys.stdin.read()
        if input_data.strip():
            new_edges = json.loads(input_data)
            for edge in new_edges:
                graph[edge["source"]].append(edge["target"])
    except:
        pass

    depths = {}
    def dfs(node, depth):
        if node not in graph or not graph[node]:
            # It's a leaf node
            if node not in depths or depth > depths[node]:
                depths[node] = depth
        else:
            for child in graph[node]:
                dfs(child, depth + 1)

    dfs("ROOT", 0)
    print(json.dumps({k: depths[k] for k in sorted(depths.keys())}))

if __name__ == "__main__":
    main()
EOF
    chmod 755 /app/oracle_etl_graph.py

    # Generate video with QR codes
    cat << 'EOF' > /app/generate_video.py
import qrcode
import json
import subprocess
import os

edges = [
    {"source": "ROOT", "target": "DB_1"},
    {"source": "ROOT", "target": "DB_2"},
    {"source": "DB_1", "target": "Collection_A"},
    {"source": "DB_1", "target": "Collection_B"},
    {"source": "DB_2", "target": "Collection_C"}
]

os.makedirs('/app/frames', exist_ok=True)
for i, edge in enumerate(edges):
    img = qrcode.make(json.dumps(edge))
    # Resize to ensure even dimensions for ffmpeg
    img = img.resize((400, 400))
    img.save(f'/app/frames/frame_{i:03d}.png')

subprocess.run([
    'ffmpeg', '-y', '-framerate', '1', '-i', '/app/frames/frame_%03d.png',
    '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p', '/app/schema_stream.mp4'
], check=True)
EOF
    python3 /app/generate_video.py
    rm -rf /app/frames /app/generate_video.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user