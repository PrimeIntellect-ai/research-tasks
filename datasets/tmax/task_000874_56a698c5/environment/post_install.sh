apt-get update && apt-get install -y python3 python3-pip git gcc build-essential valgrind espeak ffmpeg
pip3 install pytest

mkdir -p /app/repo
cd /app
espeak -w /app/voice_memo.wav "The production timezone offset is minus seven hours."

cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TZ_OFFSET -7

typedef struct {
    char* data;
} Telemetry;

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    Telemetry* t = malloc(sizeof(Telemetry));
    t->data = strdup(argv[1]);

    int len = strlen(t->data);
    for(int i=0; i<len; i++) {
        if(t->data[i] == '-') {
            t->data[i] = '_';
        }
    }

    printf("Processed: %s, TZ: %d\n", t->data, TZ_OFFSET);
    free(t->data);
    free(t);
    return 0;
}
EOF

gcc /app/oracle.c -o /app/oracle_parser
strip /app/oracle_parser
rm /app/oracle.c

cd /app/repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

cat << 'EOF' > test_regression.sh
#!/bin/bash
gcc parser.c -o test_parser
out=$(./test_parser "test-string")
if [[ "$out" == *"test_string"* && "$out" != *"X"* ]]; then
    exit 0
else
    exit 1
fi
EOF
chmod +x test_regression.sh

cat << 'EOF' > parser.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TZ_OFFSET 0

typedef struct {
    char* data;
} Telemetry;

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    Telemetry* t = malloc(sizeof(Telemetry));
    t->data = strdup(argv[1]);

    int len = strlen(t->data);
    for(int i=0; i<len; i++) {
        if(t->data[i] == '-') {
            t->data[i] = '_';
        }
    }

    printf("Processed: %s, TZ: %d\n", t->data, TZ_OFFSET);
    return 0;
}
EOF

git add parser.c test_regression.sh
git commit -m "Initial commit"

# Commit 2
echo "// comment 1" >> parser.c
git commit -am "Add comment 1"

# Commit 3 (Bad commit)
cat << 'EOF' > parser.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TZ_OFFSET 0

typedef struct {
    char* data;
} Telemetry;

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    Telemetry* t = malloc(sizeof(Telemetry));
    t->data = strdup(argv[1]);

    int len = strlen(t->data);
    for(int i=0; i<=len; i++) {
        if(t->data[i] == '-') {
            t->data[i] = '_';
        }
    }
    t->data[len] = 'X'; // Bug!

    printf("Processed: %s, TZ: %d\n", t->data, TZ_OFFSET);
    return 0;
}
EOF
git commit -am "Refactor parsing loop"

# Commit 4
echo "// comment 2" >> parser.c
git commit -am "Add comment 2"

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app