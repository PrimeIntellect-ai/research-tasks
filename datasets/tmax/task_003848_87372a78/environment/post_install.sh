apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Create auth_service.c
    cat << 'EOF' > /app/auth_service.c
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

char *base64_encode(const unsigned char *data,
                    size_t input_length,
                    size_t *output_length) {

    *output_length = 4 * ((input_length + 2) / 3);

    char *encoded_data = malloc(*output_length + 1);
    if (encoded_data == NULL) return NULL;

    for (int i = 0, j = 0; i < input_length;) {

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
        encoded_data[*output_length - 1 - i] = '=';

    encoded_data[*output_length] = '\0';
    return encoded_data;
}

int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    char *user = argv[1];
    char *perm = argv[2];
    char *token = argv[3];

    char payload[512];
    snprintf(payload, sizeof(payload), "%s|%s", user, perm);

    unsigned char xored[512];
    int len = strlen(payload);
    unsigned char key[4] = {0xDE, 0xAD, 0xBE, 0xEF};
    for (int i = 0; i < len; i++) {
        xored[i] = payload[i] ^ key[i % 4];
    }

    size_t out_len;
    char *expected_token = base64_encode(xored, len, &out_len);

    int result = strcmp(expected_token, token);
    free(expected_token);

    return result == 0 ? 0 : 1;
}
EOF

    # Compile and strip auth_service
    gcc /app/auth_service.c -o /app/auth_service
    strip /app/auth_service
    rm /app/auth_service.c

    # Create client_stub.c
    cat << 'EOF' > /home/user/client_stub.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void encode_and_print(char* user, char* perm) {
    char payload[256];
    sprintf(payload, "%s|%s", user, perm);

    // Flaw: Uses predictable PRNG (CWE-338 or CWE-334) instead of the actual static key
    srand(time(NULL));
    int key = rand(); 

    // ... base64 and XOR logic omitted for brevity ...
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user