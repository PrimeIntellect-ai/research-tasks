apt-get update && apt-get install -y python3 python3-pip gcc gdb git
    pip3 install pytest

    # Create user
    useradd -m -s /bin/bash user || true

    # Create data file
    mkdir -p /home/user/data
    python3 -c '
import os
with open("/home/user/data/server_logs.csv", "w") as f:
    for i in range(1, 1001):
        if i == 432:
            f.write(f"{i},2023-10-01T10:07:12,\n")
        else:
            f.write(f"{i},2023-10-01T10:00:00,45\n")
'

    # Create git repository
    mkdir -p /home/user/log_engine
    cd /home/user/log_engine
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"
    git checkout -b main

    # Commit 1
    cat << 'EOF' > processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_line(char *line) {
    int id, duration;
    char timestamp[64];
    if (sscanf(line, "%d,%[^,],%d", &id, timestamp, &duration) == 3) {
        // valid
    }
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        process_line(line);
    }
    fclose(f);
    return 0;
}
EOF
    git add processor.c
    git commit -m "Initial commit"
    git tag v1.0

    # Commit 2
    echo "// comment 2" >> processor.c
    git commit -am "Commit 2"

    # Commit 3
    echo "// comment 3" >> processor.c
    git commit -am "Commit 3"

    # Commit 4
    echo "// comment 4" >> processor.c
    git commit -am "Commit 4"

    # Commit 5 (Bad Commit)
    cat << 'EOF' > processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_line(char *line) {
    char *token = strtok(line, ",");
    int id = atoi(token);
    token = strtok(NULL, ","); // timestamp
    token = strtok(NULL, ","); // duration
    int duration = atoi(token); // SEGFAULT HERE ON LINE 432
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        process_line(line);
    }
    fclose(f);
    return 0;
}
EOF
    git commit -am "Performance optimization"

    # Commit 6
    echo "// comment 6" >> processor.c
    git commit -am "Commit 6"

    # Commit 7
    echo "// comment 7" >> processor.c
    git commit -am "Commit 7"

    # Commit 8
    echo "// comment 8" >> processor.c
    git commit -am "Commit 8"

    # Commit 9
    echo "// comment 9" >> processor.c
    git commit -am "Commit 9"

    # Commit 10
    echo "// comment 10" >> processor.c
    git commit -am "Commit 10"

    # Fix permissions
    chmod -R 777 /home/user