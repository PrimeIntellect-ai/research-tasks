apt-get update && apt-get install -y python3 python3-pip gcc socat netcat-openbsd
    pip3 install pytest

    mkdir -p /app/oracle /app/services

    # Create the oracle C source
    cat << 'EOF' > /app/oracle/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main() {
    uint8_t magic[4];
    if (fread(magic, 1, 4, stdin) != 4 || memcmp(magic, "BKA\x01", 4) != 0) {
        fprintf(stderr, "ERR: BAD_MAGIC\n");
        return 1;
    }
    uint32_t len;
    if (fread(&len, 4, 1, stdin) != 1) {
        fprintf(stderr, "ERR: TRUNCATED\n");
        return 2;
    }
    uint8_t *payload = malloc(len + 1);
    if (len > 0 && fread(payload, 1, len, stdin) != len) {
        fprintf(stderr, "ERR: TRUNCATED\n");
        free(payload);
        return 2;
    }
    uint32_t csum;
    if (fread(&csum, 4, 1, stdin) != 1) {
        fprintf(stderr, "ERR: TRUNCATED\n");
        free(payload);
        return 2;
    }
    uint32_t calc_csum = 0;
    for (uint32_t i = 0; i < len; i++) {
        calc_csum += payload[i];
    }
    if (calc_csum != csum) {
        fprintf(stderr, "ERR: BAD_CSUM\n");
        free(payload);
        return 3;
    }

    payload[len] = '\0';
    char *line = (char*)payload;
    char *next;
    while (line < (char*)payload + len) {
        next = strchr(line, '\n');
        if (next) {
            *next = '\0';
            if (strncmp(line, "SECRET:", 7) != 0) {
                printf("%s\n", line);
            }
            line = next + 1;
        } else {
            if (strncmp(line, "SECRET:", 7) != 0) {
                printf("%s", line);
            }
            break;
        }
    }
    free(payload);
    return 0;
}
EOF

    # Compile the oracle
    gcc -O2 -o /app/oracle/bup_filter_oracle /app/oracle/oracle.c
    rm /app/oracle/oracle.c

    # Create sender service
    cat << 'EOF' > /app/services/sender.py
import time
import socket
import struct

while True:
    try:
        s = socket.create_connection(('localhost', 7070))
        payload = b"INFO: system start\nSECRET: token=123\nWARN: low disk\n"
        L = len(payload)
        csum = sum(payload) % (2**32)
        data = b"BKA\x01" + struct.pack("<I", L) + payload + struct.pack("<I", csum)
        s.sendall(data)
        s.close()
    except Exception:
        pass
    time.sleep(1)
EOF

    # Create storage service
    cat << 'EOF' > /app/services/storage.py
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 9090))
s.listen(5)

while True:
    conn, addr = s.accept()
    data = conn.recv(4096)
    if b"INFO: system start\nWARN: low disk\n" in data and b"SECRET" not in data:
        with open("/tmp/flow_success", "w") as f:
            f.write("OK\n")
    conn.close()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user