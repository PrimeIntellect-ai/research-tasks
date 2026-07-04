apt-get update && apt-get install -y python3 python3-pip git build-essential gdb
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'SETUP_EOF' > /tmp/setup.sh
#!/bin/bash
mkdir -p "/home/user/forensics_task/data files"
cd /home/user/forensics_task

git config --global init.defaultBranch main
git config --global user.email "test@example.com"
git config --global user.name "Test User"
git init

cat << 'EOF' > Makefile
all: main
main: main.c
	gcc -g -O0 main.c -o main
EOF

cat << 'EOF' > process.sh
#!/bin/bash
export DATA_DIR="/home/user/forensics_task/data files"
./main
EOF
chmod +x process.sh

# Generate data.csv
echo "id,sensor_value" > "/home/user/forensics_task/data files/data.csv"
for i in {1..5000}; do
    if [ $i -eq 4231 ]; then
        echo "$i,105" >> "/home/user/forensics_task/data files/data.csv"
    else
        val=$((i % 50))
        echo "$i,$val" >> "/home/user/forensics_task/data files/data.csv"
    fi
done

# Commit 1: Good commit
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
int main() {
    printf("Processing complete.\n");
    return 0;
}
EOF
git add .
git commit -m "Initial commit"
git tag v1.0

# Add a few dummy commits
for i in {2..4}; do
    echo "// comment $i" >> main.c
    git commit -am "Dummy commit $i"
done

# Commit 5: Bad commit (Introduces popen without quotes and array out of bounds)
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char *data_dir = getenv("DATA_DIR");
    if (!data_dir) return 1;

    char cmd[256];
    // BUG 1: Unquoted path in shell command
    sprintf(cmd, "cat %s/data.csv", data_dir);

    FILE *fp = popen(cmd, "r");
    if (!fp) return 1;

    char line[256];
    int histogram[100] = {0};

    // skip header
    fgets(line, sizeof(line), fp);

    while (fgets(line, sizeof(line), fp)) {
        int id, val;
        if (sscanf(line, "%d,%d", &id, &val) == 2) {
            // BUG 2: No bounds check, val=105 will cause out of bounds
            histogram[val]++;
        }
    }
    pclose(fp);
    printf("Processing complete. Histogram[0]=%d\n", histogram[0]);
    return 0;
}
EOF
git commit -am "Feature: Add histogram calculation"
BAD_COMMIT=$(git rev-parse HEAD)

# Add more dummy commits
for i in {6..8}; do
    echo "// extra comment $i" >> main.c
    git commit -am "Extra commit $i"
done

# Save expected truth data
echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt
echo "4232" > /tmp/expected_anomalous_line.txt
SETUP_EOF

bash /tmp/setup.sh
chmod -R 777 /home/user