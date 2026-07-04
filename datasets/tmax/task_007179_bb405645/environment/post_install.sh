apt-get update && apt-get install -y python3 python3-pip git make gcc
    pip3 install pytest

    mkdir -p /home/user/data_processor
    cd /home/user/data_processor

    git init
    git config user.name "Test User"
    git config user.email "test@example.com"

    cat << 'EOF' > Makefile
all: data_processor
data_processor: main.c
	gcc -O2 main.c -o data_processor
EOF

    # Commit 1: v1.0 (Good)
    cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    fclose(f);
    return 0;
}
EOF
    git add Makefile main.c
    git commit -m "Initial commit v1.0"
    git tag v1.0

    # Commits 2-24: Good
    for i in {2..24}; do
        echo "// commit $i" >> main.c
        git commit -am "Refactor data processing step $i"
    done

    # Commits 25-27: Broken build (Compiler error)
    for i in {25..27}; do
        echo "this is a syntax error $i;" >> main.c
        git commit -am "WIP: optimize parsing $i"
    done

    # Commits 28-50: Bad (Intermittent failure)
    for i in {28..50}; do
        cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    fclose(f);

    // Simulate intermittent deadlock/crash on corrupted data
    srand(time(NULL) ^ getpid());
    if (rand() % 2 == 0) {
        // Intermittent hang
        sleep(2);
        return 1;
    }
    return 0;
}
EOF
        echo "// bad commit $i" >> main.c
        git commit -am "Implement new async parsing logic $i"
    done
    git tag v2.0

    # Save the expected first bad commit (which is commit 28)
    git rev-list --reverse v1.0..v2.0 | sed -n '27p' > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user