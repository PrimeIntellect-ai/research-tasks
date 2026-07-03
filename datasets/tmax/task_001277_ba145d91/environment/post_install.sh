apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app/bin /app/logs_incoming

    # Generate the voice memo audio file
    espeak -w /app/voice_memo.wav "To save space while keeping things fast, the custom archival algorithm is just a simple Run-Length Encoding. But there's a twist. It only compresses runs of null bytes, zero zero in hex. Any sequence of consecutive null bytes is replaced by a single null byte followed by a single byte indicating the count of additional null bytes in that run, up to 255. Non-null bytes are passed through exactly as they are."

    # Create dummy log files with mixed ages
    touch /app/logs_incoming/log_recent_1.log
    touch /app/logs_incoming/log_recent_2.log
    touch -d "10 days ago" /app/logs_incoming/log_old_1.log
    touch -d "8 days ago" /app/logs_incoming/log_old_2.log

    # Create archive_oracle source and compile
    cat << 'EOF' > /tmp/archive_oracle.c
#include <stdio.h>
int main() {
    int c;
    int null_count = 0;
    while ((c = fgetc(stdin)) != EOF) {
        if (c == 0) {
            null_count++;
            if (null_count == 256) {
                fputc(0, stdout);
                fputc(255, stdout);
                null_count = 1;
            }
        } else {
            if (null_count > 0) {
                fputc(0, stdout);
                fputc(null_count - 1, stdout);
                null_count = 0;
            }
            fputc(c, stdout);
        }
    }
    if (null_count > 0) {
        fputc(0, stdout);
        fputc(null_count - 1, stdout);
    }
    return 0;
}
EOF
    gcc /tmp/archive_oracle.c -o /app/bin/archive_oracle

    # Create extract_oracle source and compile
    cat << 'EOF' > /tmp/extract_oracle.c
#include <stdio.h>
int main() {
    int c;
    while ((c = fgetc(stdin)) != EOF) {
        if (c == 0) {
            int count = fgetc(stdin);
            if (count == EOF) {
                break;
            }
            for (int i = 0; i <= count; i++) {
                fputc(0, stdout);
            }
        } else {
            fputc(c, stdout);
        }
    }
    return 0;
}
EOF
    gcc /tmp/extract_oracle.c -o /app/bin/extract_oracle

    # Cleanup temporary source files
    rm /tmp/archive_oracle.c /tmp/extract_oracle.c

    # Set up user and permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app