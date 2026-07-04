apt-get update && apt-get install -y python3 python3-pip git gcc build-essential bash
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'OUTEREOF' > /tmp/setup.sh
#!/bin/bash

mkdir -p /home/user/data_pipeline
cd /home/user/data_pipeline

git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Create fake filter_tool source (good)
cat << 'EOF' > filter_tool.c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), stdin)) {
        printf("Processed %s", buffer);
    }
    return 0;
}
EOF
gcc filter_tool.c -o filter_tool

# Create pipeline.sh (good)
cat << 'EOF' > pipeline.sh
#!/bin/bash
rm -f results.txt
mkdir -p tmp_out
for i in {1..100}; do
    ( echo "Data: $i" | ./filter_tool > tmp_out/$i.txt ) &
done
wait
for i in {1..100}; do
    cat tmp_out/$i.txt >> results.txt
done
rm -rf tmp_out
EOF
chmod +x pipeline.sh

git add filter_tool.c filter_tool pipeline.sh
git commit -m "Initial commit"

# Create 50 normal commits
for i in {1..50}; do
    echo "Comment $i" >> README.md
    git add README.md
    git commit -m "Update README $i"
done

# Introduce Race Condition (Commit ~51)
cat << 'EOF' > pipeline.sh
#!/bin/bash
rm -f results.txt
for i in {1..100}; do
    ( echo "Data: $i" | ./filter_tool >> results.txt ) &
done
wait
EOF
git add pipeline.sh
git commit -m "Optimize pipeline by removing temp files"
RACE_COMMIT=$(git rev-parse HEAD)

# Create 70 normal commits
for i in {51..120}; do
    echo "Comment $i" >> README.md
    git add README.md
    git commit -m "Update README $i"
done

# Introduce Core Dump (Commit ~122)
cat << 'EOF' > filter_tool.c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), stdin)) {
        if (strncmp(buffer, "MAGIC", 5) != 0) {
            int *p = NULL;
            *p = 0; // Segfault
        }
        printf("Processed %s", buffer + 5);
        while (fgets(buffer, sizeof(buffer), stdin)) {
            printf("Processed %s", buffer);
        }
    }
    return 0;
}
EOF
gcc filter_tool.c -o filter_tool
git add filter_tool.c filter_tool
git commit -m "Update filter_tool with strict header check"
CORE_COMMIT=$(git rev-parse HEAD)

# Create 78 normal commits
for i in {121..198}; do
    echo "Comment $i" >> README.md
    git add README.md
    git commit -m "Update README $i"
done

# Save expected results somewhere secret for the verification script
mkdir -p /home/user/.secret
echo "CORE_DUMP_COMMIT=$CORE_COMMIT" > /home/user/.secret/expected_commits.txt
echo "RACE_CONDITION_COMMIT=$RACE_COMMIT" >> /home/user/.secret/expected_commits.txt
OUTEREOF

    chmod +x /tmp/setup.sh
    /tmp/setup.sh
    rm /tmp/setup.sh

    chown -R user:user /home/user
    chmod -R 777 /home/user