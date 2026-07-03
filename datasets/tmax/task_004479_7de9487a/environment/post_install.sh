apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Generate the image with the hidden threshold
    convert -size 600x200 canvas:white -font DejaVu-Sans -pointsize 24 -fill black -draw "text 20,50 'System configuration update:' text 20,90 'Set DEADLOCK_THRESHOLD_MS=4500 to prevent' text 20,130 'false positives during high load spikes.'" /app/system_notes.png

    # Create the reference detector (oracle) in Python
    cat << 'EOF' > /app/reference_detector_src.py
#!/usr/bin/env python3
import sys
import csv

threshold = 4500
graph = {}
nodes = set()

for row in csv.reader(sys.stdin):
    if not row: continue
    u, v, wait, prio = map(int, row)
    nodes.add(u)
    nodes.add(v)
    if wait > threshold:
        graph[u] = {'v': v, 'wait': wait, 'prio': prio}

visited = set()
path = []
cycles = []

def dfs(node):
    if node in path:
        idx = path.index(node)
        cycles.append(path[idx:])
        return
    if node in visited:
        return
    visited.add(node)
    path.append(node)
    if node in graph:
        dfs(graph[node]['v'])
    path.pop()

for n in nodes:
    dfs(n)

victims = []
# Process isolated cycles
for cycle in cycles:
    cycle_nodes = []
    for u in cycle:
        cycle_nodes.append((u, graph[u]['prio'], graph[u]['wait']))

    # Sort criteria: min priority, then min wait time, then max tx_id
    cycle_nodes.sort(key=lambda x: (x[1], x[2], -x[0]))
    victims.append(cycle_nodes[0][0])

for v in sorted(list(set(victims))):
    print(v)
EOF

    chmod +x /app/reference_detector_src.py
    mv /app/reference_detector_src.py /app/reference_detector

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user