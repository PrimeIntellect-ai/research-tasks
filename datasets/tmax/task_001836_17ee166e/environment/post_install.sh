apt-get update && apt-get install -y python3 python3-pip gcc tesseract-ocr
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate the image
    cat << 'EOF' > /tmp/gen_image.py
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (800, 300), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = """EntityMap
Entity: Employee -> Node: Worker, RecursiveEdge: MANAGES
Entity: Customer -> Node: Client, RecursiveEdge: REFERRED
Entity: Product -> Node: Item, RecursiveEdge: REPLACES"""
d.text((10, 10), text, fill=(0, 0, 0))
img.save('/app/schema_rules.png')
EOF
    python3 /tmp/gen_image.py

    # Create the oracle
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>

void get_mapping(const char* entity, char* node, char* edge) {
    if (strcmp(entity, "Employee") == 0) {
        strcpy(node, "Worker");
        strcpy(edge, "MANAGES");
    } else if (strcmp(entity, "Customer") == 0) {
        strcpy(node, "Client");
        strcpy(edge, "REFERRED");
    } else if (strcmp(entity, "Product") == 0) {
        strcpy(node, "Item");
        strcpy(edge, "REPLACES");
    } else {
        strcpy(node, "Unknown");
        strcpy(edge, "UNKNOWN");
    }
}

int main() {
    char cmd[256];
    char ent1[256], ent2[256], id1[256], id2[256];
    int depth;
    while (scanf("%s", cmd) != EOF) {
        if (strcmp(cmd, "MATCH_HIERARCHY") == 0) {
            scanf("%s %s %d", ent1, id1, &depth);
            char node[64], edge[64];
            get_mapping(ent1, node, edge);
            printf("MATCH (n:%s {id: \"%s\"})-[r:%s*1..%d]->(m:%s) RETURN n, r, m;\n", node, id1, edge, depth, node);
        } else if (strcmp(cmd, "AGGREGATE_REACH") == 0) {
            scanf("%s %s", ent1, id1);
            char node[64], edge[64];
            get_mapping(ent1, node, edge);
            printf("MATCH (n:%s {id: \"%s\"})-[:%s*]->(m:%s) RETURN count(DISTINCT m) as total_reach;\n", node, id1, edge, node);
        } else if (strcmp(cmd, "FIND_INTERSECT") == 0) {
            scanf("%s %s %s %s", ent1, id1, ent2, id2);
            char node1[64], edge1[64], node2[64], edge2[64];
            get_mapping(ent1, node1, edge1);
            get_mapping(ent2, node2, edge2);
            printf("MATCH (a:%s {id: \"%s\"})-->(common)<--(b:%s {id: \"%s\"}) RETURN common;\n", node1, id1, node2, id2);
        }
    }
    return 0;
}
EOF
    gcc -O3 /tmp/oracle.c -o /app/oracle_cypher_gen

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user