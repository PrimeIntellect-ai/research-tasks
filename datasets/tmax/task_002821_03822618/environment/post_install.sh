apt-get update && apt-get install -y python3 python3-pip gcc make git gdb
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/repo
cd /home/user/repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

cat << 'EOF' > data_parser.c
#include <stdio.h>
#include <string.h>

void process_file(const char *filepath) {
    char secret_key[] = "DEBUG_KEY_7734";
    printf("Processing: %s\n", filepath);
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    process_file(argv[1]);
    return 0;
}
EOF

cat << 'EOF' > Makefile
all: data_parser

data_parser: data_parser.c
	gcc -g -O0 -o data_parser data_parser.c

test: data_parser
	./data_parser "normal_file.txt"
	./data_parser "file with spaces"
EOF

git add data_parser.c Makefile
git commit -m "Initial commit"
git tag v1.0

for i in $(seq 1 150); do
    echo "// comment $i" >> data_parser.c
    git commit -am "Commit $i"
done

cat << 'EOF' > data_parser.c
#include <stdio.h>
#include <string.h>

void process_file(const char *filepath) {
    char secret_key[] = "DEBUG_KEY_7734";
    printf("Processing: %s\n", filepath);
    char *space = strchr(filepath, ' ');
    if (space != NULL) {
        char *ext = strchr(space, '.');
        int len = strlen(ext); // Crash here if ext is NULL
        printf("Extension length: %d\n", len);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    process_file(argv[1]);
    return 0;
}
EOF

echo "// comment 151" >> data_parser.c
git commit -am "Commit 151"
BAD_COMMIT=$(git rev-parse HEAD)
echo "$BAD_COMMIT" > /home/user/.secret_bad_commit

for i in $(seq 152 200); do
    echo "// comment $i" >> data_parser.c
    git commit -am "Commit $i"
done

chown -R user:user /home/user/repo
chmod -R 777 /home/user