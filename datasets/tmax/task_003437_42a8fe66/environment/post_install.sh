apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app

    # Generate the voice memo
    espeak -w /app/voicememo.wav "The archive format starts with the magic bytes B A C K. Then it repeats entries until EOF. Each entry is a two-byte little endian unsigned integer for the file name length, then the file name string, then a four-byte little endian unsigned integer for the file size, then the file data itself. To prevent zip slip, if any file name contains the exact substring dot dot slash ('../'), you must completely skip that entry and not print anything for it. For all valid entries, print the filename, a colon, and the file size, followed by a newline."

    # Create the oracle C program
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main() {
    char magic[4];
    if (fread(magic, 1, 4, stdin) != 4) return 0;
    if (memcmp(magic, "BACK", 4) != 0) return 1;

    while (1) {
        uint16_t name_len;
        if (fread(&name_len, 1, 2, stdin) != 2) break;
        char *name = malloc(name_len + 1);
        if (fread(name, 1, name_len, stdin) != name_len) { free(name); break; }
        name[name_len] = '\0';

        uint32_t file_size;
        if (fread(&file_size, 1, 4, stdin) != 4) { free(name); break; }

        // Skip file data
        char buf[4096];
        uint32_t rem = file_size;
        while (rem > 0) {
            uint32_t to_read = rem > 4096 ? 4096 : rem;
            size_t r = fread(buf, 1, to_read, stdin);
            if (r == 0) break;
            rem -= r;
        }
        if (rem > 0) { free(name); break; }

        if (strstr(name, "../") == NULL) {
            printf("%s:%u\n", name, file_size);
        }
        free(name);
    }
    return 0;
}
EOF

    # Compile the oracle and strip it
    gcc -O2 /app/oracle.c -o /app/oracle_archive_tool
    strip /app/oracle_archive_tool
    rm /app/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user