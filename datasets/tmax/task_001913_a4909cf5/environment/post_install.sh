apt-get update && apt-get install -y python3 python3-pip git gcc gdb
    pip3 install pytest

    mkdir -p /home/user/app_repo
    cd /home/user/app_repo

    git init
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    # Create the data file
    cat << 'EOF' > data.csv
1,apple
2,banana
3,cherry
4,date
EOF

    # Create the Python test script
    cat << 'EOF' > test_build.py
import subprocess
import sqlite3
import sys

def main():
    # Compile
    res = subprocess.run(["gcc", "-g", "-o", "process", "process.c"])
    if res.returncode != 0:
        print("Compilation failed")
        sys.exit(1)

    # Run
    res = subprocess.run(["./process", "data.csv"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Execution failed")
        sys.exit(1)

    sql_inserts = res.stdout

    # Test DB
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")

    try:
        for line in sql_inserts.strip().split('\n'):
            if line:
                cursor.execute(line)
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
        sys.exit(1)

    cursor.execute("SELECT COUNT(*) FROM records")
    count = cursor.fetchone()[0]

    if count != 4:
        print(f"Query Result Error: Expected 4 records, got {count}")
        sys.exit(1)

    print("Build and tests passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
EOF

    # Create build.sh
    cat << 'EOF' > build.sh
#!/bin/bash
python3 test_build.py
EOF
    chmod +x build.sh

    # Initial working C program
    cat << 'EOF' > process.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int ids[10];
    char names[10][50];
    int count = 0;

    char line[100];
    while (fgets(line, sizeof(line), f)) {
        sscanf(line, "%d,%[^\n]", &ids[count], names[count]);
        count++;
    }
    fclose(f);

    for (int i = 0; i < count; i++) {
        printf("INSERT INTO records VALUES (%d, '%s');\n", ids[i], names[i]);
    }
    return 0;
}
EOF

    git add .
    git commit -m "Initial commit: working version"
    GOOD_COMMIT=$(git rev-parse HEAD)

    # Commit 2: Add some comments
    echo "// Added data processing" >> process.c
    git commit -am "Add comments"

    # Commit 3: Introduce the bug (Off-by-one error)
    cat << 'EOF' > process.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Added data processing
int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int ids[10];
    char names[10][50];
    int count = 0;

    char line[100];
    while (fgets(line, sizeof(line), f)) {
        sscanf(line, "%d,%[^\n]", &ids[count], names[count]);
        count++;
    }
    fclose(f);

    for (int i = 0; i <= count; i++) {
        printf("INSERT INTO records VALUES (%d, '%s');\n", ids[i], names[i]);
    }
    return 0;
}
EOF
    git commit -am "Refactor loop boundary"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 4: Add README
    echo "# App Repo" > README.md
    git add README.md
    git commit -m "Add README"

    # Commit 5: Unrelated change
    echo "// End of file" >> process.c
    git commit -am "Minor cleanup"

    # Save the truth internally
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/app_repo
    chmod -R 777 /home/user