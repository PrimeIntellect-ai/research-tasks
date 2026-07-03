apt-get update && apt-get install -y python3 python3-pip git gcc make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/data_processor
    cd /home/user/data_processor
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    cat << 'EOF' > parse_time.c
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    printf("Processed %s\n", argv[1]);
    return 0;
}
EOF

    cat << 'EOF' > Makefile
all:
	gcc -o parse_time parse_time.c
EOF

    cat << 'EOF' > process_logs.sh
#!/bin/bash
grep '2023-01-01' "$1" | wc -l
EOF
    chmod +x process_logs.sh

    cat << 'EOF' > test_input.log
2023-01-01T10:00:00Z
2023-01-01T23:00:00Z
2023-01-02T02:00:00Z
EOF

    git add .
    git commit -m "Initial commit"

    # 100 good commits
    for i in $(seq 1 99); do
        echo "// comment $i" >> parse_time.c
        git commit -am "Good commit $i"
    done

    # Introduce logic bug (Commit 101)
    cat << 'EOF' > process_logs.sh
#!/bin/bash
# Buggy version: filters out late night events due to bad timezone shift
grep '2023-01-01T1' "$1" | wc -l
EOF
    git commit -am "Update log processing logic"
    git rev-parse HEAD > /tmp/ground_truth_commit.txt

    # 49 buggy but compiling commits
    for i in $(seq 101 149); do
        echo "// comment $i" >> parse_time.c
        git commit -am "Buggy commit $i"
    done

    # Introduce compile error (Commit 151)
    cat << 'EOF' > parse_time.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc, char **argv) {
    if (argc < 2) return 1;
    double val = sqrt(atof(argv[1]));
    printf("Processed %f\n", val);
    return 0;
}
EOF
    git commit -am "Add advanced math processing"

    # 50 broken commits
    for i in $(seq 151 200); do
        echo "// comment $i" >> parse_time.c
        git commit -am "Broken commit $i"
    done

    chown -R user:user /home/user/data_processor
    chmod -R 777 /home/user