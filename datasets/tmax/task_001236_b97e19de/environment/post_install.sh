apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick gcc fonts-dejavu
pip3 install pytest

mkdir -p /app

# Create the query image
convert -background white -fill black -font DejaVu-Sans -pointsize 24 label:"MATCH (A)-[:LINK]->(B)-[:LINK]->(C)\nWHERE A.id % 2 = 0 AND C.id % 3 = 0\nRETURN A.id, C.id" /app/query.png

# Create the oracle C program
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int src;
    int dst;
} Edge;

int cmp_edges(const void *a, const void *b) {
    Edge *ea = (Edge *)a;
    Edge *eb = (Edge *)b;
    if (ea->src != eb->src) return ea->src - eb->src;
    return ea->dst - eb->dst;
}

int main() {
    int src, dst;
    int capacity = 10000;
    int num_edges = 0;
    Edge *edges = malloc(capacity * sizeof(Edge));

    while (scanf("%d %d", &src, &dst) == 2) {
        if (num_edges >= capacity) {
            capacity *= 2;
            edges = realloc(edges, capacity * sizeof(Edge));
        }
        edges[num_edges].src = src;
        edges[num_edges].dst = dst;
        num_edges++;
    }

    int out_cap = 10000;
    int num_out = 0;
    Edge *out = malloc(out_cap * sizeof(Edge));

    for (int i = 0; i < num_edges; i++) {
        int A = edges[i].src;
        int B = edges[i].dst;
        if (A % 2 != 0) continue;

        for (int j = 0; j < num_edges; j++) {
            if (edges[j].src == B) {
                int C = edges[j].dst;
                if (C % 3 == 0) {
                    if (num_out >= out_cap) {
                        out_cap *= 2;
                        out = realloc(out, out_cap * sizeof(Edge));
                    }
                    out[num_out].src = A;
                    out[num_out].dst = C;
                    num_out++;
                }
            }
        }
    }

    qsort(out, num_out, sizeof(Edge), cmp_edges);

    for (int i = 0; i < num_out; i++) {
        if (i > 0 && out[i].src == out[i-1].src && out[i].dst == out[i-1].dst) continue;
        printf("%d,%d\n", out[i].src, out[i].dst);
    }

    free(edges);
    free(out);
    return 0;
}
EOF

gcc -O3 -o /app/oracle_projector /app/oracle.c
chmod +x /app/oracle_projector

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user