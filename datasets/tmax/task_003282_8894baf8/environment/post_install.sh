apt-get update && apt-get install -y python3 python3-pip gcc gdb coreutils
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user

    cat << 'EOF' > processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_data(const char *input) {
    char buffer[64];
    // Vulnerability: strcpy without bounds checking
    strcpy(buffer, input);
    printf("Processed: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *data = malloc(fsize + 1);
    fread(data, 1, fsize, f);
    data[fsize] = '\0';
    fclose(f);

    process_data(data);
    free(data);
    return 0;
}
EOF

    gcc -g -fno-stack-protector -O0 processor.c -o processor

    echo -n "Normal payload data" | base64 > payload1.b64
    echo -n "Another normal payload" | base64 > payload2.b64
    python3 -c "print('A'*80, end='')" > crash_input.bin
    base64 crash_input.bin > payload_crash.b64

    cat << EOF > service.log
[2023-10-27 02:55:01] INFO TXN-1001 Processed payload: $(cat payload1.b64)
[2023-10-27 02:58:14] INFO TXN-1002 Processed payload: $(cat payload2.b64)
[2023-10-27 03:00:00] INFO TXN-1003 Processed payload: $(cat payload_crash.b64)
EOF

    # Generate core dump using gdb to bypass container ulimit issues
    gdb --batch -ex "run crash_input.bin" -ex "generate-core-file core" ./processor || true

    # Fallback if gdb failed to generate core
    if [ ! -f core ]; then
        ulimit -c unlimited || true
        ./processor crash_input.bin || true
        mv core* core 2>/dev/null || touch core
    fi

    rm payload1.b64 payload2.b64 payload_crash.b64 crash_input.bin

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user