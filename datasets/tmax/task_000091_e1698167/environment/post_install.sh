apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/legacy_sim/data
    cd /home/user/legacy_sim

    cat << 'EOF' > config.py
SECRET_KEY = "legacy_sim_key_992"
EOF

    cat << 'EOF' > calculator.py
def compute_precise_sum(n):
    # BUG: uses standard float, leading to precision loss
    total = 0.0
    for _ in range(n):
        total += 0.1
    return total
EOF

    cat << 'EOF' > tree_resolver.py
def count_nodes(start_node_id, graph_data, visited=None):
    # BUG: Does not utilize the visited set to stop cycles
    node = graph_data.get(start_node_id)
    if not node:
        return 0
    count = 1
    for child in node.get('children', []):
        count += count_nodes(child, graph_data)
    return count
EOF

    cat << 'EOF' > data/graph.json
{
    "A": {"children": ["B"]},
    "B": {"children": ["C", "D"]},
    "C": {"children": ["A"]},
    "D": {"children": []}
}
EOF

    cat << 'EOF' > generate_report.py
import sys
import json
from calculator import compute_precise_sum
from tree_resolver import count_nodes

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_report.py <SECRET_KEY>")
        sys.exit(1)

    key = sys.argv[1]
    if key != "legacy_sim_key_992":
        print("Error: Invalid secret key.")
        sys.exit(1)

    # Check precision fix
    val = compute_precise_sum(10)
    if str(val) != "1.0" or type(val).__name__ != "Decimal":
        print("Error: calculator.py is not returning the correct decimal.Decimal value.")
        sys.exit(1)

    # Check recursion fix
    with open("data/graph.json", "r") as f:
        graph = json.load(f)

    try:
        count = count_nodes("A", graph)
        if count != 4:
            print(f"Error: tree_resolver.py returned {count} instead of 4 unique nodes.")
            sys.exit(1)
    except RecursionError:
        print("Error: RecursionError in tree_resolver.py.")
        sys.exit(1)

    print("SUCCESS: VALIDATION_PASSED_FLAG_88219")

if __name__ == "__main__":
    main()
EOF

    git init
    git config user.email "dev@example.com"
    git config user.name "Developer"
    git add .
    git commit -m "Initial commit with project skeleton"

    cat << 'EOF' > config.py
SECRET_KEY = ""
EOF
    git add config.py
    git commit -m "Removed secret key for security"

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user