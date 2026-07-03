apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Create oracle C++ source
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <set>
#include <map>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) return 1;
    ifstream infile(argv[1]);
    string line;
    map<string, set<string>> adj;
    vector<string> nodes;
    set<string> node_set;
    while (getline(infile, line)) {
        stringstream ss(line);
        string src, dst, type;
        double weight;
        if (ss >> src >> dst >> type >> weight) {
            if (weight > 5.0) {
                adj[src].insert(dst);
            }
            node_set.insert(src);
            node_set.insert(dst);
        }
    }
    for (auto n : node_set) nodes.push_back(n);

    set<string> result;
    // O(V^3) naive approach
    for (size_t i = 0; i < nodes.size(); ++i) {
        for (size_t j = 0; j < nodes.size(); ++j) {
            if (adj[nodes[i]].count(nodes[j])) {
                for (size_t k = 0; k < nodes.size(); ++k) {
                    if (adj[nodes[j]].count(nodes[k]) && adj[nodes[k]].count(nodes[i])) {
                        result.insert(nodes[i]);
                        result.insert(nodes[j]);
                        result.insert(nodes[k]);
                    }
                }
            }
        }
    }

    for (const auto& node : result) {
        cout << node << endl;
    }
    return 0;
}
EOF

    # Compile and strip the binary
    g++ -O0 /tmp/oracle.cpp -o /app/motif_oracle
    strip /app/motif_oracle

    # Generate graph datasets
    cat << 'EOF' > /tmp/generate_graphs.py
import random
random.seed(42)

def generate_graph(num_edges, num_nodes, num_cycles, filename):
    edges = []
    # Add random edges
    for _ in range(num_edges - num_cycles * 3):
        src = f"n{random.randint(1, num_nodes)}"
        dst = f"n{random.randint(1, num_nodes)}"
        weight = round(random.uniform(1.0, 10.0), 2)
        edges.append((src, dst, "rel", weight))

    # Add cycles
    for _ in range(num_cycles):
        n1 = f"n{random.randint(1, num_nodes)}"
        n2 = f"n{random.randint(1, num_nodes)}"
        n3 = f"n{random.randint(1, num_nodes)}"
        edges.append((n1, n2, "rel", round(random.uniform(5.1, 10.0), 2)))
        edges.append((n2, n3, "rel", round(random.uniform(5.1, 10.0), 2)))
        edges.append((n3, n1, "rel", round(random.uniform(5.1, 10.0), 2)))

    random.shuffle(edges)
    with open(filename, "w") as f:
        for e in edges:
            f.write(f"{e[0]}\t{e[1]}\t{e[2]}\t{e[3]}\n")

generate_graph(500, 50, 3, "/home/user/sample_edges.tsv")
generate_graph(50000, 1000, 100, "/home/user/eval_edges.tsv")
EOF

    python3 /tmp/generate_graphs.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user