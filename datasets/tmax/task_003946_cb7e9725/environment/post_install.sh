apt-get update && apt-get install -y python3 python3-pip gcc make valgrind libcjson-dev
    pip3 install pytest

    mkdir -p /app/cJSON-1.7.15
    mkdir -p /app/bin

    # Create dummy cJSON files
    echo "/* cJSON dummy */" > /app/cJSON-1.7.15/cJSON.c
    echo "/* cJSON header */" > /app/cJSON-1.7.15/cJSON.h

    # Create telemetry_processor.c
    cat << 'EOF' > /app/telemetry_processor.c
#include <stdio.h>
int main() {
    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), stdin)) {
        printf("%s", buffer);
    }
    return 0;
}
EOF

    # Create Makefile
    cat << 'EOF' > /app/Makefile
all:
	gcc telemetry_processor.c -o telemetry_processor -lcjson
EOF

    # Create oracle_processor
    cat << 'EOF' > /app/bin/oracle_processor.c
#include <stdio.h>
int main() {
    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), stdin)) {
        printf("%s", buffer);
    }
    return 0;
}
EOF
    gcc /app/bin/oracle_processor.c -o /app/bin/oracle_processor
    rm /app/bin/oracle_processor.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app