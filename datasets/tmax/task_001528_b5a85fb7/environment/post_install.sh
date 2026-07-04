apt-get update && apt-get install -y python3 python3-pip gcc make valgrind gdb
    pip3 install pytest

    mkdir -p /home/user/service
    cd /home/user/service

    cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-g -Wall -Wextra

all: tx_service

tx_service: main.o tx_proc.o
	$(CC) $(CFLAGS) -o $@ $^

EOF
    echo "%.o: %.c" >> Makefile
    echo "	\$(CC) \$(CFLAGS) -c \$<" >> Makefile
    cat << 'EOF' >> Makefile

clean:
	rm -f *.o tx_service
EOF

    cat << 'EOF' > tx_proc.h
#ifndef TX_PROC_H
#define TX_PROC_H

void process_transaction(const char* hex_payload);

#endif
EOF

    cat << 'EOF' > tx_proc.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "tx_proc.h"

// Helper to convert hex char to int
int hex_char_to_int(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}

void process_transaction(const char* hex_payload) {
    size_t len = strlen(hex_payload);
    assert(len % 2 == 0); // Must be valid hex string length

    size_t decoded_len = len / 2;
    char* decoded_buffer = (char*)malloc(decoded_len + 1);
    if (!decoded_buffer) return;

    for (size_t i = 0; i < decoded_len; i++) {
        int high = hex_char_to_int(hex_payload[i * 2]);
        int low = hex_char_to_int(hex_payload[i * 2 + 1]);
        decoded_buffer[i] = (char)((high << 4) | low);
    }
    decoded_buffer[decoded_len] = '\0';

    // Simulate validation
    if (strncmp(decoded_buffer, "ERR_TX_", 7) == 0) {
        // Validation failed, early exit. BUG: Missing free(decoded_buffer);
        fprintf(stderr, "Transaction error detected. Aborting.\n");
        return; 
    }

    printf("Processed successfully: %s\n", decoded_buffer);

    free(decoded_buffer);
}
EOF

    cat << 'EOF' > main.c
#include "tx_proc.h"
#include <stdio.h>

int main() {
    // Valid: "OK_TX_001" -> 4f4b5f54585f303031
    process_transaction("4f4b5f54585f303031");

    // Valid: "OK_TX_002" -> 4f4b5f54585f303032
    process_transaction("4f4b5f54585f303032");

    // Invalid (Triggers leak): "ERR_TX_99482A" -> 4552525f54585f393934383241
    process_transaction("4552525f54585f393934383241");

    // Valid: "OK_TX_003" -> 4f4b5f54585f303033
    process_transaction("4f4b5f54585f303033");

    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user