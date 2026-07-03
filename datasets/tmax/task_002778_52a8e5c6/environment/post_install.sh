apt-get update && apt-get install -y python3 python3-pip gcc espeak
pip3 install pytest

mkdir -p /app

cat << 'EOF' > /app/oracle_parser.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;

    char magic[8];
    if (fread(magic, 1, 8, f) != 8 || memcmp(magic, "WALDATA1", 8) != 0) {
        fclose(f);
        return 1;
    }

    uint64_t reclaimable = 0;
    uint32_t len;
    uint8_t type;

    while (fread(&len, 4, 1, f) == 1) {
        if (fread(&type, 1, 1, f) != 1) break;
        if (type == 4) {
            reclaimable += len;
        }
        fseek(f, len, SEEK_CUR);
    }

    printf("Reclaimable: %llu bytes\n", (unsigned long long)reclaimable);
    fclose(f);
    return 0;
}
EOF

gcc -O3 /app/oracle_parser.c -o /app/oracle_parser
strip /app/oracle_parser
rm /app/oracle_parser.c

espeak -w /app/voicemail.wav "The WAL format starts with the magic string 'WALDATA1'. After the 8-byte magic string, there is a sequence of records. Each record consists of a 4-byte unsigned little-endian integer representing the payload length, followed immediately by a 1-byte record type, followed by the payload itself. To calculate reclaimable space, you must write a script that sums the payload lengths of all records of type 4. Print the final result exactly as 'Reclaimable: X bytes'."

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user