apt-get update && apt-get install -y python3 python3-pip ffmpeg gawk coreutils
    pip3 install pytest

    mkdir -p /app
    mkdir -p /opt/verifier

    # Generate a dummy video file
    ffmpeg -f lavfi -i color=c=black:s=100x100:d=1 -vframes 120 /app/transaction_monitor.mp4

    # Create the oracle program
    cat << 'EOF' > /opt/verifier/reference_deadlock_detector.sh
#!/usr/bin/env python3
import sys, csv
from collections import defaultdict

def find_cycles(graph):
    cycles = []
    visited = set()
    path = []

    def dfs(node):
        if node in path:
            cycle = path[path.index(node):]
            cycles.append(sorted(list(set(cycle))))
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        path.pop()

    for node in list(graph.keys()):
        dfs(node)

    unique_cycles = []
    for c in cycles:
        if c not in unique_cycles:
            unique_cycles.append(c)
    return unique_cycles

def main():
    if len(sys.argv) < 2: return
    locks = {}
    wait_for = defaultdict(list)
    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == 'timestamp': continue
            _, tx, res = row
            if res not in locks:
                locks[res] = tx
            elif locks[res] != tx:
                if locks[res] not in wait_for[tx]:
                    wait_for[tx].append(locks[res])

    cycles = find_cycles(wait_for)
    for c in cycles:
        print(",".join(c))

if __name__ == '__main__':
    main()
EOF
    chmod +x /opt/verifier/reference_deadlock_detector.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user