apt-get update && apt-get install -y python3 python3-pip gcc rustc cargo acl expect
    pip3 install pytest

    mkdir -p /app/corpus_samples/clean /app/corpus_samples/evil
    mkdir -p /app/verifier/corpus/clean /app/verifier/corpus/evil

    # Create clean files
    cat << 'EOF' > /app/corpus_samples/clean/1.json
{"urgency": 5, "msg": "All good"}
EOF
    cat << 'EOF' > /app/corpus_samples/clean/2.json
{"urgency": 10, "msg": "Warning level 10"}
EOF
    cp /app/corpus_samples/clean/*.json /app/verifier/corpus/clean/

    # Create evil files
    cat << 'EOF' > /app/corpus_samples/evil/1.json
{"urgency": 11, "msg": "Too urgent"}
EOF
    cat << 'EOF' > /app/corpus_samples/evil/2.json
{"urgency": 5, "msg": "Please DROP TABLE users;"}
EOF
    cat << 'EOF' > /app/corpus_samples/evil/3.json
{"urgency": 5, "msg": "Price is $100"}
EOF
    cat << 'EOF' > /app/corpus_samples/evil/4.json
{"urgency": 5, "msg": "Pipe | symbol"}
EOF
    cat << 'EOF' > /app/corpus_samples/evil/5.json
{"urgency": 5, "msg": "Backtick ` symbol"}
EOF
    cat << 'EOF' > /app/corpus_samples/evil/6.json
{"urgency": 5, "msg": "Semicolon ; symbol"}
EOF
    cat << 'EOF' > /app/corpus_samples/evil/7.json
{invalid json
EOF
    head -c 1025 /dev/urandom > /app/corpus_samples/evil/8.json

    cp /app/corpus_samples/evil/* /app/verifier/corpus/evil/

    # Create the oracle C program
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    printf("Enter Passphrase: ");
    char pass[256];
    if (!fgets(pass, sizeof(pass), stdin)) return 1;
    if (strncmp(pass, "monitor_auth_99", 15) != 0) {
        printf("[REJECT]\n");
        return 1;
    }
    setenv("TARGET_FILE", argv[1], 1);
    int ret = system("python3 -c \"\n"
"import sys, json, re, os\n"
"try:\n"
"    with open(os.environ['TARGET_FILE'], 'rb') as f:\n"
"        data = f.read()\n"
"    if len(data) > 1024: sys.exit(1)\n"
"    j = json.loads(data)\n"
"    if j.get('urgency', 0) > 10: sys.exit(1)\n"
"    msg = j.get('msg', '')\n"
"    if 'drop table' in msg.lower(): sys.exit(1)\n"
"    if re.search(r'[\\$\\|\\;\\`]', msg): sys.exit(1)\n"
"    sys.exit(0)\n"
"except Exception as e:\n"
"    sys.exit(1)\n"
"\" > /dev/null 2>&1");
    if (ret == 0) {
        printf("[VALID]\n");
        return 0;
    } else {
        printf("[REJECT]\n");
        return 1;
    }
}
EOF
    gcc -O2 /tmp/oracle.c -o /app/log_oracle
    strip /app/log_oracle
    rm /tmp/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user