apt-get update && apt-get install -y python3 python3-pip git gcc make gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/parser_repo
    cd /home/user/parser_repo
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    cat << 'EOF' > main.c
#include <stdio.h>
#include <string.h>

void process(const char* name) {
    printf("Processing %s\n", name);
}

int main(int argc, char** argv) {
    if (argc > 1) { process(argv[1]); }
    return 0;
}
EOF
    cat << 'EOF' > Makefile
all:
	gcc -g -O0 main.c -o parser
clean:
	rm -f parser
EOF
    git add main.c Makefile
    git commit -m "Initial commit"

    for i in $(seq 1 25); do
        echo "// minor refactor $i" >> main.c
        git commit -am "Commit $i"
    done

    cat << 'EOF' > main.c
#include <stdio.h>
#include <string.h>

void process(const char* name) {
    char *space = strchr(name, ' ');
    if (space) {
        char *target = NULL;
        *target = '_';
    }
    printf("Processing %s\n", name);
}

int main(int argc, char** argv) {
    if (argc > 1) { process(argv[1]); }
    return 0;
}
EOF
    git commit -am "Refactor process function to handle spaces"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo "$BAD_COMMIT" > /tmp/expected_commit.txt

    for i in $(seq 27 50); do
        echo "// minor refactor $i" >> main.c
        git commit -am "Commit $i"
    done

    cat << 'EOF' > /home/user/test.sh
#!/bin/bash
cd /home/user/parser_repo
make clean > /dev/null 2>&1
make > /dev/null 2>&1
./parser "data file.txt"
EOF
    chmod +x /home/user/test.sh

    chown -R user:user /home/user/parser_repo /home/user/test.sh
    chmod -R 777 /home/user