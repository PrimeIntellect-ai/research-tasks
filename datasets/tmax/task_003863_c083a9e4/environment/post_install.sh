apt-get update && apt-get install -y python3 python3-pip gcc espeak ffmpeg
    pip3 install pytest

    mkdir -p /app
    mkdir -p /etc/archival

    # Generate voicemail.wav
    espeak -w /app/voicemail.wav "Hey, it's Dave. Make sure the new script only archives files larger than 50 megabytes, and only apply it to log and bak extensions."

    # Create legacy policies
    cat << 'EOF' > /etc/archival/legacy_policies.conf
# Legacy Policies
EXCLUDE_DIR=/var/tmp
EXCLUDE_DIR=/tmp
MIN_AGE_DAYS=30
EOF

    # Create oracle C source
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static const char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                      'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                      'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                      'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                      'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                      'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                      'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                      '4', '5', '6', '7', '8', '9', '+', '/'};
static const int mod_table[] = {0, 2, 1};

void base64_encode(const unsigned char *data, size_t input_length, char *encoded_data) {
    size_t output_length = 4 * ((input_length + 2) / 3);
    for (size_t i = 0, j = 0; i < input_length;) {
        uint32_t octet_a = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;
        encoded_data[j++] = encoding_table[(triple >> 3 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 2 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 1 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 0 * 6) & 0x3F];
    }
    for (int i = 0; i < mod_table[input_length % 3]; i++)
        encoded_data[output_length - 1 - i] = '=';
    encoded_data[output_length] = '\0';
}

int main() {
    char line[8192];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\n")] = 0;
        char *last_space = strrchr(line, ' ');
        if (!last_space) continue;
        long long ts = atoll(last_space + 1);
        *last_space = 0;

        char *second_last_space = strrchr(line, ' ');
        if (!second_last_space) continue;
        long long size = atoll(second_last_space + 1);
        *second_last_space = 0;

        char *path = line;

        if (size > 52428800) {
            int len = strlen(path);
            if ((len > 4 && (strcmp(path + len - 4, ".log") == 0 || strcmp(path + len - 4, ".bak") == 0)) &&
                strncmp(path, "/var/tmp/", 9) != 0 && strncmp(path, "/tmp/", 5) != 0) {
                char b64[8192];
                base64_encode((const unsigned char*)path, len, b64);
                printf("ARCHIVE_REQ|%s|%lld\n", b64, size / 1024);
            }
        }
    }
    return 0;
}
EOF

    gcc -O2 /app/oracle.c -o /app/oracle_archive_filter
    rm /app/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user