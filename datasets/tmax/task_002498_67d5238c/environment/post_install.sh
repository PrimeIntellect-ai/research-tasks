apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install gcc for compiling C programs and imagemagick for generating the image
    apt-get install -y gcc imagemagick fonts-dejavu-core

    # Create app directory
    mkdir -p /app

    # Generate the schema diagram image
    # Note: %% is used to escape the % character in ImageMagick labels
    convert -background white -fill black -font DejaVu-Sans -pointsize 24 label:"CYPHER MAPPING TEMPLATE: MERGE (r:Researcher {res_id: %%d})-[:PUBLISHED_IN]->(j:Journal {issn: '%%s'})" /app/schema_diagram.png

    # Create the oracle program
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
int main() {
    int id;
    char issn[32];
    while (scanf("%d,%31s", &id, issn) == 2) {
        printf("MERGE (r:Researcher {res_id: %d})-[:PUBLISHED_IN]->(j:Journal {issn: '%s'})\n", id, issn);
    }
    return 0;
}
EOF

    # Compile the oracle program
    gcc -O2 /app/oracle.c -o /app/oracle_build_queries
    chmod +x /app/oracle_build_queries

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user