apt-get update && apt-get install -y python3 python3-pip gcc make
pip3 install pytest

# Create directories
mkdir -p /app/libkggraph-1.2.0/src
mkdir -p /app/libkggraph-1.2.0/include
mkdir -p /opt/oracle

# Create libkggraph.h
cat << 'EOF' > /app/libkggraph-1.2.0/include/libkggraph.h
#ifndef LIBKGGRAPH_H
#define LIBKGGRAPH_H

typedef struct kg_graph_t kg_graph_t;
kg_graph_t* kg_create(int num_nodes);
void kg_add_edge(kg_graph_t* g, int u, int v, int role);
int kg_check_transitive(kg_graph_t* g, int start_node, int end_node, int min_role);
void kg_destroy(kg_graph_t* g);

#endif
EOF

# Create graph.c
cat << 'EOF' > /app/libkggraph-1.2.0/src/graph.c
#include <stdlib.h>
#include "../include/libkggraph.h"

typedef struct edge_t {
    int v;
    int role;
    struct edge_t* next;
} edge_t;

struct kg_graph_t {
    int num_nodes;
    edge_t** adj;
};

kg_graph_t* kg_create(int num_nodes) {
    kg_graph_t* g = malloc(sizeof(kg_graph_t));
    g->num_nodes = num_nodes;
    g->adj = calloc(num_nodes, sizeof(edge_t*));
    return g;
}

void kg_add_edge(kg_graph_t* g, int u, int v, int role) {
    if (u < 0 || u >= g->num_nodes || v < 0 || v >= g->num_nodes) return;
    edge_t* e = malloc(sizeof(edge_t));
    e->v = v;
    e->role = role;
    e->next = g->adj[u];
    g->adj[u] = e;
}

void kg_destroy(kg_graph_t* g) {
    for (int i = 0; i < g->num_nodes; i++) {
        edge_t* e = g->adj[i];
        while (e) {
            edge_t* next = e->next;
            free(e);
            e = next;
        }
    }
    free(g->adj);
    free(g);
}
EOF

# Create traversal.c
cat << 'EOF' > /app/libkggraph-1.2.0/src/traversal.c
#include <stdlib.h>
#include "../include/libkggraph.h"

#ifndef MAX_DEPTH
#define MAX_DEPTH 1024
#endif

typedef struct edge_t {
    int v;
    int role;
    struct edge_t* next;
} edge_t;

struct kg_graph_t {
    int num_nodes;
    edge_t** adj;
};

static int dfs(kg_graph_t* g, int u, int end_node, int min_role, int* visited, int depth) {
    if (u == end_node) return 1;
    if (depth >= MAX_DEPTH) return 0;
    visited[u] = 1;
    for (edge_t* e = g->adj[u]; e; e = e->next) {
        if (e->role >= min_role && !visited[e->v]) {
            if (dfs(g, e->v, end_node, min_role, visited, depth + 1)) {
                return 1;
            }
        }
    }
    return 0;
}

int kg_check_transitive(kg_graph_t* g, int start_node, int end_node, int min_role) {
    if (start_node < 0 || start_node >= g->num_nodes) return 0;
    int* visited = calloc(g->num_nodes, sizeof(int));
    int res = dfs(g, start_node, end_node, min_role, visited, 0);
    free(visited);
    return res;
}
EOF

# Create Makefile
cat << 'EOF' > /app/libkggraph-1.2.0/Makefile
CC = gcc
CFLAGS = -O2 -Wall -DMAX_DEPTH=1
AR = ar

all: libkggraph.a

libkggraph.a: src/graph.o src/traversal.o
	$(AR) rcs $@ $^

src/graph.o: src/graph.c
	$(CC) $(CFLAGS) -c $< -o $@

src/traversal.o: src/traversal.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f src/*.o libkggraph.a
EOF

# Compile the library initially
cd /app/libkggraph-1.2.0 && make

# Create oracle program source
cat << 'EOF' > /opt/oracle/checker_oracle.c
#include <stdio.h>
#include <stdlib.h>

typedef struct edge_t {
    int v;
    int role;
    struct edge_t* next;
} edge_t;

static int dfs(int u, int end_node, int min_role, int* visited, edge_t** adj) {
    if (u == end_node) return 1;
    visited[u] = 1;
    for (edge_t* e = adj[u]; e; e = e->next) {
        if (e->role >= min_role && !visited[e->v]) {
            if (dfs(e->v, end_node, min_role, visited, adj)) {
                return 1;
            }
        }
    }
    return 0;
}

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    edge_t** adj = calloc(n, sizeof(edge_t*));
    for (int i = 0; i < m; i++) {
        int u, v, r;
        if (scanf("%d %d %d", &u, &v, &r) == 3) {
            edge_t* e = malloc(sizeof(edge_t));
            e->v = v;
            e->role = r;
            e->next = adj[u];
            adj[u] = e;
        }
    }
    int q;
    if (scanf("%d", &q) != 1) return 0;
    for (int i = 0; i < q; i++) {
        int x, y;
        if (scanf("%d %d", &x, &y) == 2) {
            int* visited = calloc(n, sizeof(int));
            printf("%d\n", dfs(x, y, 3, visited, adj));
            free(visited);
        }
    }
    return 0;
}
EOF

# Compile oracle
gcc -O2 /opt/oracle/checker_oracle.c -o /opt/oracle/checker_oracle

# Create user
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app/libkggraph-1.2.0