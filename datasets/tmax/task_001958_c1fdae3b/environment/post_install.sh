apt-get update && apt-get install -y python3 python3-pip build-essential
    pip3 install pytest

    mkdir -p /app/custom_httpd-1.0.0/src
    mkdir -p /app/custom_httpd-1.0.0/include
    mkdir -p /opt/verifier

    # Create Makefile with intentional typo
    cat << 'EOF' > /app/custom_httpd-1.0.0/Makefile
CC=gccc
CFLAGS=-I./include -Wall

all: custom_httpd

custom_httpd: src/main.o src/request_handler.o
	$(CC) -o custom_httpd src/main.o src/request_handler.o

src/main.o: src/main.c
	$(CC) $(CFLAGS) -c src/main.c -o src/main.o

src/request_handler.o: src/request_handler.c
	$(CC) $(CFLAGS) -c src/request_handler.c -o src/request_handler.o
EOF

    # Create dummy main.c
    cat << 'EOF' > /app/custom_httpd-1.0.0/src/main.c
#include <stdio.h>

int main() {
    printf("Starting server...\n");
    return 0;
}
EOF

    # Create vulnerable request_handler.c
    cat << 'EOF' > /app/custom_httpd-1.0.0/src/request_handler.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void handle_request(const char *query) {
    char cmd[512];
    // Command injection vulnerability
    snprintf(cmd, sizeof(cmd), "echo %s > /tmp/log", query);
    system(cmd);

    // XSS vulnerability
    printf("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n");
    printf("<html><body>Search results for: %s</body></html>\n", query);
}
EOF

    # Generate access.log
    cat << 'EOF' > /app/access.log
192.168.1.10 - - [10/Oct/2023:13:55:36 -0700] "GET /search?q=apple HTTP/1.1" 200 2326
192.168.1.100 - - [10/Oct/2023:13:55:37 -0700] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 200 2326
192.168.1.101 - - [10/Oct/2023:13:55:38 -0700] "GET /search?q=test;cat /etc/passwd HTTP/1.1" 200 2326
192.168.1.12 - - [10/Oct/2023:13:55:39 -0700] "GET /search?q=banana HTTP/1.1" 200 2326
EOF

    # Create ground truth file
    cat << 'EOF' > /opt/verifier/ground_truth_ips.txt
192.168.1.100
192.168.1.101
EOF

    # Create evaluate script
    cat << 'EOF' > /opt/verifier/evaluate.py
#!/usr/bin/env python3
import sys
import os

def evaluate():
    if not os.path.exists("/home/user/malicious_ips.txt"):
        print("malicious_ips.txt not found")
        sys.exit(1)

    with open("/opt/verifier/ground_truth_ips.txt") as f:
        truth = set(f.read().splitlines())

    with open("/home/user/malicious_ips.txt") as f:
        preds = set(f.read().splitlines())

    tp = len(truth.intersection(preds))
    fp = len(preds - truth)
    fn = len(truth - preds)

    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    print(f"F1 Score: {f1}")
    if f1 >= 0.95:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    evaluate()
EOF
    chmod +x /opt/verifier/evaluate.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user