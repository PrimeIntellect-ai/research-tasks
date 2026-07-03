apt-get update && apt-get install -y python3 python3-pip gcc make git libpcap-dev
pip3 install pytest scapy

useradd -m -s /bin/bash user || true

mkdir -p /home/user/netdaemon
cd /home/user/netdaemon

cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-g -Wall -pthread
LDFLAGS=-lpcap -pthread

all: netdaemon

netdaemon: main.c parser.c worker.c
	$(CC) $(CFLAGS) -o netdaemon main.c parser.c worker.c $(LDFLAGS)

clean:
	rm -f netdaemon
EOF

cat << 'EOF' > netdaemon.h
#ifndef NETDAEMON_H
#define NETDAEMON_H

#include <stdint.h>
#include <pcap.h>
#include <pthread.h>

extern uint64_t total_bytes_processed;
extern pthread_mutex_t stats_mutex;

void process_packet(const u_char *payload, int len);
int parse_tlv(const u_char *data, int len, int depth);

#endif
EOF

cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <pthread.h>
#include "netdaemon.h"

uint64_t total_bytes_processed = 0;
pthread_mutex_t stats_mutex = PTHREAD_MUTEX_INITIALIZER;

void packet_handler(u_char *user, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    // Skip Ethernet, IP, and UDP headers for simplicity in this dummy test (assume 42 bytes)
    if (pkthdr->len > 42) {
        process_packet(packet + 42, pkthdr->len - 42);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <pcap_file>\n", argv[0]);
        return 1;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_open_offline(argv[1], errbuf);
    if (handle == NULL) {
        fprintf(stderr, "Error opening pcap: %s\n", errbuf);
        return 1;
    }

    pcap_loop(handle, 0, packet_handler, NULL);
    pcap_close(handle);

    printf("Total bytes: %lu\n", total_bytes_processed);
    return 0;
}
EOF

cat << 'EOF' > worker.c
#include "netdaemon.h"
#include <unistd.h>

void process_packet(const u_char *payload, int len) {
    parse_tlv(payload, len, 0);
    // RACE CONDITION HERE
    uint64_t temp = total_bytes_processed;
    usleep(10); // Artificial delay to force race condition
    total_bytes_processed = temp + len;
}
EOF

cat << 'EOF' > parser.c_v1
#include "netdaemon.h"
#include <stdio.h>

int parse_tlv(const u_char *data, int len, int depth) {
    if (len < 2) return 0;
    int type = data[0];
    int length = data[1];
    if (length > len - 2) return 0;

    // safe version
    if (length == 0) return 0;
    if (type == 1) { // Nested TLV
        parse_tlv(data + 2, length, depth + 1);
    }
    return 1;
}
EOF

cat << 'EOF' > parser.c_v2
#include "netdaemon.h"
#include <stdio.h>

int parse_tlv(const u_char *data, int len, int depth) {
    if (len < 2) return 0;
    int type = data[0];
    int length = data[1];
    if (length > len - 2) return 0;

    // BAD COMMIT: Removed length == 0 check, causing infinite recursion
    if (type == 1) { // Nested TLV
        parse_tlv(data + 2, length, depth + 1);
    }
    return 1;
}
EOF

cat << 'EOF' > test_hang.sh
#!/bin/bash
make clean > /dev/null 2>&1
make > /dev/null 2>&1
# test with a dummy payload that has type=1, len=0
echo -ne '\x01\x00' > dummy.bin
timeout 1 ./netdaemon dummy.bin > /dev/null 2>&1
if [ $? -eq 124 ]; then
    exit 1 # Hang detected
else
    exit 0 # OK
fi
EOF
chmod +x test_hang.sh

git init
git config user.email "ops@example.com"
git config user.name "Ops"

cp parser.c_v1 parser.c
git add .
git commit -m "Initial commit"

for i in {1..3}; do
    echo "// Comment $i" >> main.c
    git commit -am "Update main.c #$i"
done

cp parser.c_v2 parser.c
git commit -am "Refactor parser logic to handle nested TLVs better"
BAD_COMMIT=$(git rev-parse HEAD)
echo $BAD_COMMIT > /tmp/true_bad_commit.txt

for i in {4..6}; do
    echo "// Comment $i" >> main.c
    git commit -am "Update main.c #$i"
done

cat << 'EOF' > /tmp/gen_pcap.py
from scapy.all import *
packets = []
# Valid packet
p1 = Ether()/IP(dst="127.0.0.1")/UDP(dport=1234)/Raw(load=b'\x02\x04test')
# Malformed packet triggering recursion (type=1, len=0)
p2 = Ether()/IP(dst="127.0.0.1")/UDP(dport=1234)/Raw(load=b'\x01\x00')
# Valid packet
p3 = Ether()/IP(dst="127.0.0.1")/UDP(dport=1234)/Raw(load=b'\x02\x02ok')

wrpcap('/home/user/traffic.pcap', [p1, p1, p2, p3, p1])
EOF
python3 /tmp/gen_pcap.py

chmod -R 777 /home/user