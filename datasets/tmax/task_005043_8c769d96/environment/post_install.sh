apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest hypothesis

    mkdir -p /app

    # Create the oracle binary
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
int main() {
    int c;
    while ((c = getchar()) != EOF) {
        unsigned char b = (unsigned char)c;
        b = (b ^ 0x4B) + 17;
        putchar(b);
    }
    return 0;
}
EOF
    gcc -o /app/oracle_bin /app/oracle.c
    rm /app/oracle.c

    # Generate the audio specification file
    espeak -w /app/spec.wav "The obfuscation algorithm is as follows: first, XOR each byte with hexadecimal four B. Then, add decimal seventeen modulo two hundred fifty six."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user