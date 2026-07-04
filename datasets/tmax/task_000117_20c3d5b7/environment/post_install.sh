apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest
    apt-get install -y git sqlite3 gcc bsdmainutils build-essential

    mkdir -p /home/user/pipeline_repo
    cd /home/user/pipeline_repo
    git init
    git branch -m main
    git config user.name "Tester"
    git config user.email "test@example.com"

    # 1. Create the binary
    mkdir -p bin
    cat << 'EOF' > validator.c
#include <stdlib.h>
int main(int argc, char** argv) {
    if(argc < 2) return 1;
    int val = atoi(argv[1]);
    if(val >= 32 && val <= 212) return 0;
    return 1;
}
EOF
    gcc validator.c -o bin/validator
    rm validator.c

    # 2. Create process.sh
    cat << 'EOF' > process.sh
#!/bin/bash
db="$1"
if [ -z "$db" ]; then echo "No db provided"; exit 1; fi
temp_c=$(sqlite3 "$db" "SELECT temp FROM readings LIMIT 1;")
if [ -z "$temp_c" ]; then echo "No temp found"; exit 1; fi

# Convert to Fahrenheit
temp_f=$(( (temp_c * 9 / 5) + 32 ))

./bin/validator $temp_f
exit $?
EOF
    chmod +x process.sh

    git add bin/validator process.sh
    git commit -m "Initial commit"
    git tag v1.0

    # Add 140 good commits
    for i in $(seq 2 140); do
        echo "# update $i" >> process.sh
        git commit -am "Minor update $i"
    done

    # Introduce bug at commit 141
    sed -i 's/+ 32/- 32/' process.sh
    git commit -am "Refactor formula"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # Add 59 bad commits
    for i in $(seq 142 200); do
        echo "# update $i" >> process.sh
        git commit -am "Minor update $i"
    done

    # 3. Create and corrupt database
    sqlite3 sensor.db "CREATE TABLE readings(temp INTEGER);"
    sqlite3 sensor.db "INSERT INTO readings(temp) VALUES (20);"
    # Corrupt the SQLite header so standard queries fail
    dd if=/dev/urandom of=sensor.db bs=1 count=16 conv=notrunc

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user