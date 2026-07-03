apt-get update && apt-get install -y python3 python3-pip gcc imagemagick tesseract-ocr fonts-liberation
    pip3 install pytest

    # Create /app directory and generate the cypher template image
    mkdir -p /app
    convert -background white -fill black -font Courier -pointsize 18 label:"TEMPLATE REQUIRED:\nMATCH (n1:Account {id: '%s'}), (n2:Account {id: '%s'})\nSET %s.balance = %s.balance - %d, %s.balance = %s.balance + %d\nRETURN n1.id, n2.id;" /app/cypher_template.png

    # Create oracle source code
    cat << 'EOF' > /opt/oracle_query_builder.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char line[1024];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (strlen(line) == 0) continue;

        char tx[256], from[256], to[256];
        int amount;
        if (sscanf(line, "%[^,],%[^,],%[^,],%d", tx, from, to, &amount) == 4) {
            if (strcmp(from, to) == 0) continue;

            char *n1_id, *n2_id;
            char *from_alias, *to_alias;

            if (strcmp(from, to) < 0) {
                n1_id = from;
                n2_id = to;
                from_alias = "n1";
                to_alias = "n2";
            } else {
                n1_id = to;
                n2_id = from;
                from_alias = "n2";
                to_alias = "n1";
            }

            printf("MATCH (n1:Account {id: '%s'}), (n2:Account {id: '%s'})\n", n1_id, n2_id);
            printf("SET %s.balance = %s.balance - %d, %s.balance = %s.balance + %d\n", from_alias, from_alias, amount, to_alias, to_alias, amount);
            printf("RETURN n1.id, n2.id;\n");
        }
    }
    return 0;
}
EOF

    # Compile the oracle
    gcc -O3 /opt/oracle_query_builder.c -o /opt/oracle_query_builder

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user