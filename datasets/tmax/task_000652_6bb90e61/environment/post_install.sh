apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app

    # Generate audio
    espeak -w /app/audit_memo.wav "Here are the requirements for the auditor tool. The program must read exactly 32 bytes from stdin. First, we need to prevent disguised binaries. If the first four bytes match the standard ELF magic number—that's hex 7F followed by E, L, F—print 'ERROR: DISGUISED ELF'. If it's not an ELF, we check the permissions. Read the two bytes at offset 4 as a little-endian 16-bit integer. If the setuid bit is set—meaning the bitwise AND with hex 0800, which is octal 04000, is non-zero—print 'ALERT: SUID'. If neither of those triggered, check for a basic exploit payload. If the four bytes from offset 16 to 19 are all hex 90, representing a NOP sled, print 'ERROR: PAYLOAD DETECTED'. If none of these conditions are met, simply print 'PASS'."

    # Generate oracle
    cat << 'EOF' > /app/oracle_auditor.c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main() {
    unsigned char buf[32];
    if (fread(buf, 1, 32, stdin) != 32) return 1;

    if (buf[0] == 0x7F && buf[1] == 'E' && buf[2] == 'L' && buf[3] == 'F') {
        printf("ERROR: DISGUISED ELF\n");
    } else {
        uint16_t perms = buf[4] | (buf[5] << 8);
        if (perms & 0x0800) {
            printf("ALERT: SUID\n");
        } else if (buf[16] == 0x90 && buf[17] == 0x90 && buf[18] == 0x90 && buf[19] == 0x90) {
            printf("ERROR: PAYLOAD DETECTED\n");
        } else {
            printf("PASS\n");
        }
    }
    return 0;
}
EOF
    gcc -O2 /app/oracle_auditor.c -o /app/oracle_auditor
    rm /app/oracle_auditor.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user