apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    mkdir -p /app

    # Compile oracle
    cat << 'C_EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NODES 1000
#define MAX_NAME 16

typedef struct {
    char name[MAX_NAME];
    int in_degree;
    int edges[MAX_NODES];
    int edge_count;
} Node;

Node nodes[MAX_NODES];
int node_count = 0;

int get_or_add_node(const char* name) {
    for (int i = 0; i < node_count; i++) {
        if (strcmp(nodes[i].name, name) == 0) return i;
    }
    strcpy(nodes[node_count].name, name);
    nodes[node_count].in_degree = 0;
    nodes[node_count].edge_count = 0;
    return node_count++;
}

int main() {
    char line[64];
    while (fgets(line, sizeof(line), stdin)) {
        char src[32], dst[32];
        if (sscanf(line, "%[^:]:%s", src, dst) == 2) {
            int u = get_or_add_node(src);
            int v = get_or_add_node(dst);
            nodes[u].edges[nodes[u].edge_count++] = v;
            nodes[v].in_degree++;
        }
    }

    int sorted[MAX_NODES];
    int sorted_count = 0;
    int visited[MAX_NODES] = {0};

    while (sorted_count < node_count) {
        int best_idx = -1;
        for (int i = 0; i < node_count; i++) {
            if (!visited[i] && nodes[i].in_degree == 0) {
                if (best_idx == -1 || strcmp(nodes[i].name, nodes[best_idx].name) < 0) {
                    best_idx = i;
                }
            }
        }
        if (best_idx == -1) {
            printf("{\"error\": \"cycle_detected\"}\n");
            return 0;
        }
        visited[best_idx] = 1;
        sorted[sorted_count++] = best_idx;
        for (int i = 0; i < nodes[best_idx].edge_count; i++) {
            nodes[nodes[best_idx].edges[i]].in_degree--;
        }
    }

    printf("[");
    for (int i = 0; i < sorted_count; i++) {
        printf("\"%s\"", nodes[sorted[i]].name);
        if (i < sorted_count - 1) printf(", ");
    }
    printf("]\n");
    return 0;
}
C_EOF
    gcc -O3 /tmp/oracle.c -o /app/oracle_resolver
    strip /app/oracle_resolver || true

    # Create Video Fixture with subtitle
    cat << 'SRT_EOF' > /tmp/subs.srt
1
00:00:00,000 --> 00:00:05,000
InitDB:StartServer
StartServer:AcceptRequests
AcceptRequests:ProcessData
InitDB:ProcessData
AuthModule:AcceptRequests
SRT_EOF

    ffmpeg -f lavfi -i color=c=black:s=320x240:d=5 -i /tmp/subs.srt -c:v libx264 -c:s mov_text -map 0:v -map 1:s /app/architecture.mp4 -y

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user