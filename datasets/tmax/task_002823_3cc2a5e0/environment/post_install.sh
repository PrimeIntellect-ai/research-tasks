apt-get update && apt-get install -y python3 python3-pip g++ libcurl4-openssl-dev curl netcat
    pip3 install pytest flask

    mkdir -p /app/services
    mkdir -p /home/user/pipeline

    # Create Graph API
    cat << 'EOF' > /app/services/graph_api.py
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/neighbors/<int:node_id>')
def neighbors(node_id):
    return jsonify([node_id + 1, node_id + 2])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    # Create Event TCP Server
    cat << 'EOF' > /app/services/event_tcp.py
import socket
import threading

def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if b"PULL" in data:
                # event_id,node_id,value,timestamp
                # Return some static events
                resp = "1,2,10,100\n2,2,20,101\n3,3,30,102\n4,4,40,103\n"
                conn.sendall(resp.encode('utf-8'))

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 5001))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == '__main__':
    start_server()
EOF

    # Create buggy C++ aggregator
    cat << 'EOF' > /home/user/pipeline/aggregator.cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>

struct Event {
    int event_id;
    int node_id;
    int value;
    int timestamp;
};

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        int query_node = std::stoi(line);

        // Mock fetch neighbors
        std::vector<int> neighbors = {query_node + 1, query_node + 2};

        // Mock fetch events
        std::vector<Event> events = {
            {1, 2, 10, 100},
            {2, 2, 20, 101},
            {3, 3, 30, 102},
            {4, 4, 40, 103}
        };

        std::vector<int> results;
        int rolling_sum = 0;

        // BUGGY LOGIC
        for (int neighbor : neighbors) {
            for (auto& event : events) {
                // Implicit cross join: missing `if (event.node_id == neighbor)`
                rolling_sum += event.value;
                results.push_back(rolling_sum);
            }
        }

        std::cout << "Query: " << query_node << " | Rolling Sums: [";
        for (size_t i = 0; i < results.size(); ++i) {
            std::cout << results[i] << (i + 1 == results.size() ? "" : ", ");
        }
        std::cout << "]\n";
    }
    return 0;
}
EOF

    # Create fixed C++ aggregator (Oracle)
    cat << 'EOF' > /tmp/oracle_aggregator.cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>

struct Event {
    int event_id;
    int node_id;
    int value;
    int timestamp;
};

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        int query_node = std::stoi(line);

        std::vector<int> neighbors = {query_node + 1, query_node + 2};

        std::vector<Event> events = {
            {1, 2, 10, 100},
            {2, 2, 20, 101},
            {3, 3, 30, 102},
            {4, 4, 40, 103}
        };

        std::vector<int> results;

        for (int neighbor : neighbors) {
            int rolling_sum = 0;
            for (auto& event : events) {
                if (event.node_id == neighbor) {
                    rolling_sum += event.value;
                    results.push_back(rolling_sum);
                }
            }
        }

        std::cout << "Query: " << query_node << " | Rolling Sums: [";
        for (size_t i = 0; i < results.size(); ++i) {
            std::cout << results[i] << (i + 1 == results.size() ? "" : ", ");
        }
        std::cout << "]\n";
    }
    return 0;
}
EOF

    g++ -O2 -std=c++17 /tmp/oracle_aggregator.cpp -o /app/oracle_aggregator
    chmod +x /app/oracle_aggregator

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user