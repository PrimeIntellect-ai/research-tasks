apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest networkx

    useradd -m -s /bin/bash user || true

    mkdir -p /app/kg-path-finder-0.9/src

    cat << 'EOF' > /app/kg-path-finder-0.9/Makefile
CC = gcc
CFLAGS = -Wall -g -O0

all: kg-path-finder

kg-path-finder: src/main.c src/graph.c src/bfs.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f kg-path-finder
EOF

    cat << 'EOF' > /app/kg-path-finder-0.9/src/graph.h
#ifndef GRAPH_H
#define GRAPH_H

typedef struct {
    int num_nodes;
    int *row_ptr;
    int *col_ind;
} Graph;

Graph* load_graph(const char *filename);
void free_graph(Graph *g);
int compute_shortest_path(Graph *graph, int source, int target);

#endif
EOF

    cat << 'EOF' > /app/kg-path-finder-0.9/src/graph.c
#include <stdio.h>
#include <stdlib.h>
#include "graph.h"

Graph* load_graph(const char *filename) {
    FILE *f = fopen(filename, "r");
    if (!f) return NULL;
    int u, v;
    int max_node = -1;
    int edges = 0;
    while (fscanf(f, "%d\t%d", &u, &v) == 2) {
        if (u > max_node) max_node = u;
        if (v > max_node) max_node = v;
        edges++;
    }

    Graph *g = malloc(sizeof(Graph));
    g->num_nodes = max_node + 1;
    g->row_ptr = calloc(g->num_nodes + 2, sizeof(int));

    rewind(f);
    while (fscanf(f, "%d\t%d", &u, &v) == 2) {
        g->row_ptr[u + 1]++;
    }
    for (int i = 0; i < g->num_nodes; i++) {
        g->row_ptr[i+1] += g->row_ptr[i];
    }
    g->col_ind = malloc(edges * sizeof(int));
    int *cur_ptr = malloc((g->num_nodes + 1) * sizeof(int));
    for (int i = 0; i <= g->num_nodes; i++) cur_ptr[i] = g->row_ptr[i];

    rewind(f);
    while (fscanf(f, "%d\t%d", &u, &v) == 2) {
        g->col_ind[cur_ptr[u]++] = v;
    }
    free(cur_ptr);
    fclose(f);
    return g;
}

void free_graph(Graph *g) {
    free(g->row_ptr);
    free(g->col_ind);
    free(g);
}
EOF

    cat << 'EOF' > /app/kg-path-finder-0.9/src/bfs.c
#include <stdlib.h>
#include <string.h>
#include "graph.h"

int compute_shortest_path(Graph *graph, int source, int target) {
    if (source == target) return 0;
    if (source >= graph->num_nodes || target >= graph->num_nodes) return -1;

    int *visited = calloc(graph->num_nodes, sizeof(int));
    memset(visited, 0, graph->num_nodes * sizeof(int) / 2);

    int *queue = malloc(graph->num_nodes * sizeof(int));
    int *dist = calloc(graph->num_nodes, sizeof(int));

    int head = 0, tail = 0;
    queue[tail++] = source;
    visited[source] = 1;
    dist[source] = 0;

    int found_dist = -1;

    while (head < tail) {
        int u = queue[head++];
        if (u == target) {
            found_dist = dist[u];
            break;
        }
        int start = graph->row_ptr[u];
        int end = graph->row_ptr[u+1];
        for (int i = start; i < end; i++) {
            int v = graph->col_ind[i];
            if (!visited[v]) {
                visited[v] = 1;
                dist[v] = dist[u] + 1;
                queue[tail++] = v;
            }
        }
    }

    free(visited);
    free(queue);
    free(dist);
    return found_dist;
}
EOF

    cat << 'EOF' > /app/kg-path-finder-0.9/src/main.c
#include <stdio.h>
#include <stdlib.h>
#include "graph.h"

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <graph.tsv> <queries.tsv>\n", argv[0]);
        return 1;
    }
    Graph *g = load_graph(argv[1]);
    if (!g) return 1;

    FILE *qf = fopen(argv[2], "r");
    if (!qf) return 1;

    int u, v;
    while (fscanf(qf, "%d\t%d", &u, &v) == 2) {
        int d = compute_shortest_path(g, u, v);
        printf("%d,%d,%d\n", u, v, d);
    }
    fclose(qf);
    free_graph(g);
    return 0;
}
EOF

    cat << 'EOF' > /tmp/generate_data.py
import networkx as nx
import random
import csv

num_nodes = 50000
num_edges = 200000
num_queries = 10000

G = nx.gnm_random_graph(num_nodes, num_edges, directed=True, seed=42)

with open('/home/user/bio_network.tsv', 'w') as f:
    for u, v in G.edges():
        f.write(f"{u}\t{v}\n")

nodes = list(G.nodes())
queries = []
random.seed(42)
for _ in range(num_queries):
    u = random.choice(nodes)
    v = random.choice(nodes)
    queries.append((u, v))

with open('/home/user/protein_queries.tsv', 'w') as f:
    for u, v in queries:
        f.write(f"{u}\t{v}\n")

with open('/tmp/golden_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for u, v in queries:
        try:
            d = nx.shortest_path_length(G, u, v)
        except nx.NetworkXNoPath:
            d = -1
        writer.writerow([u, v, d])
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    chmod -R 777 /app
    chmod -R 777 /home/user