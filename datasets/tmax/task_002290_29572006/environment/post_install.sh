apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app
    useradd -m -s /bin/bash user || true

    # Generate voicemail audio
    espeak -w /app/voicemail.wav "Please filter out any edge with a latency strictly greater than one hundred. Also, for any edge where the target node ID is a multiple of five, add a penalty of ten to its latency."

    # Create oracle source
    cat << 'EOF' > /app/oracle_source.c
#include <stdio.h>
#include <stdlib.h>

#define MAX_NODES 10005

typedef struct Edge {
    int target;
    int weight;
    struct Edge* next;
} Edge;

Edge* graph[MAX_NODES];

void add_edge(int u, int v, int w) {
    if (w > 100) return; // Filter rule
    if (v % 5 == 0) w += 10; // Penalty rule

    Edge* e = malloc(sizeof(Edge));
    e->target = v;
    e->weight = w;
    e->next = graph[u];
    graph[u] = e;
}

int dijkstra(int start, int end) {
    int dist[MAX_NODES];
    int visited[MAX_NODES] = {0};
    for(int i=0; i<MAX_NODES; i++) dist[i] = 1e9;
    dist[start] = 0;

    for(int i=0; i<MAX_NODES; i++) {
        int u = -1;
        for(int j=0; j<MAX_NODES; j++) {
            if(!visited[j] && (u == -1 || dist[j] < dist[u])) {
                u = j;
            }
        }
        if(dist[u] == 1e9) break;
        visited[u] = 1;
        if(u == end) return dist[u];

        for(Edge* e = graph[u]; e != NULL; e = e->next) {
            if(dist[u] + e->weight < dist[e->target]) {
                dist[e->target] = dist[u] + e->weight;
            }
        }
    }
    return dist[end] == 1e9 ? -1 : dist[end];
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    FILE* f = fopen(argv[1], "r");
    if (!f) return 1;
    int u, v, w;
    while(fscanf(f, "%d,%d,%d", &u, &v, &w) == 3) {
        add_edge(u, v, w);
    }
    fclose(f);

    while(scanf("%d %d", &u, &v) == 2) {
        printf("%d\n", dijkstra(u, v));
    }
    return 0;
}
EOF

    # Compile oracle
    gcc -O3 /app/oracle_source.c -o /app/oracle_engine

    # Generate CSV files
    cat << 'EOF' > /app/generate_csv.py
import random

def generate(filename, num_nodes, num_edges):
    with open(filename, 'w') as f:
        for _ in range(num_edges):
            u = random.randint(0, num_nodes-1)
            v = random.randint(0, num_nodes-1)
            w = random.randint(1, 150)
            f.write(f"{u},{v},{w}\n")

generate('/home/user/network.csv', 1000, 100000)
generate('/app/test_network.csv', 1000, 100000)
EOF

    python3 /app/generate_csv.py

    chmod -R 777 /app
    chmod -R 777 /home/user