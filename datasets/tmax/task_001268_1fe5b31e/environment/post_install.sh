apt-get update && apt-get install -y python3 python3-pip gcc xxd
    pip3 install pytest scapy

    # Create app directory
    mkdir -p /app/custom_net_parser

    # Create vendored package
    cat << 'EOF' > /app/custom_net_parser/__init__.py
from .core import parse
EOF

    cat << 'EOF' > /app/custom_net_parser/core.py
import struct

def parse(data: bytes):
    if len(data) < 4:
        raise ValueError("Too short")
    if data[0] != 0x88:
        raise ValueError("Invalid protocol ID")

    flag = data[1]
    # BUG: Should be payload_len = struct.unpack('>H', data[2:4])[0]
    payload_len = struct.unpack('>B', data[2:3])[0]

    payload = data[4 : 4 + payload_len]

    # This will throw struct.error if the remaining slice is not exactly 2 bytes
    checksum = struct.unpack('>H', data[4 + payload_len :])[0]

    return {
        "protocol": 0x88,
        "flag": flag,
        "payload_len": payload_len,
        "payload_hex": payload.hex(),
        "checksum": checksum
    }
EOF

    # Create Oracle C program
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int hex2bin(const char *hex, uint8_t *bin) {
    int len = strlen(hex);
    for(int i=0; i<len/2; i++) {
        sscanf(hex + 2*i, "%2hhx", &bin[i]);
    }
    return len/2;
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    uint8_t data[2048];
    int len = hex2bin(argv[1], data);

    if (len < 4) return 1;
    if (data[0] != 0x88) return 1;

    uint8_t flag = data[1];
    uint16_t payload_len = (data[2] << 8) | data[3];

    if (len != 4 + payload_len + 2) return 1;

    printf("{\"protocol\": 136, \"flag\": %d, \"payload_len\": %d, \"payload_hex\": \"", flag, payload_len);
    for(int i=0; i<payload_len; i++) {
        printf("%02x", data[4+i]);
    }
    uint16_t checksum = (data[4+payload_len] << 8) | data[4+payload_len+1];
    printf("\", \"checksum\": %d}\n", checksum);
    return 0;
}
EOF
    gcc -o /app/oracle_parser /tmp/oracle.c
    rm /tmp/oracle.c

    # Generate diagnostic pcap using scapy
    cat << 'EOF' > /tmp/gen_pcap.py
from scapy.all import wrpcap, Ether, IP, UDP
import struct

# Create a packet that triggers the bug.
# The bug reads 1 byte for length (01) instead of 2 bytes (01 05 = 261).
# We need a packet where the correct length is 261, so the packet must be 4 + 261 + 2 = 267 bytes long.
payload = bytes.fromhex("88010105") + (b"\x00" * 261) + bytes.fromhex("FFFF")
pkt = Ether()/IP(dst="127.0.0.1")/UDP(dport=1234)/payload

wrpcap("/app/diagnostic_capture.pcap", [pkt])
EOF
    python3 /tmp/gen_pcap.py
    rm /tmp/gen_pcap.py

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /app
    chmod -R 777 /home/user
    chmod -R 777 /app