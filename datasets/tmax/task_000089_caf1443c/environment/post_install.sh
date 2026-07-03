apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

# Install necessary system packages
apt-get install -y curl tar gcc make libc-dev sed

# Create directories and download cJSON
mkdir -p /app
curl -sL https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.tar.gz | tar -xz -C /app
sed -i 's/#include <string.h>/#include <strnig.h>/g' /app/cJSON-1.7.15/cJSON.c

# Compile the Oracle
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int main() {
    char buffer[1024];
    if (!fgets(buffer, sizeof(buffer), stdin)) return 1;
    buffer[strcspn(buffer, "\r\n")] = 0;

    char *pipe_pos = strchr(buffer, '|');
    if (!pipe_pos) {
        printf("ERR: FORMAT\n");
        return 1;
    }
    *pipe_pos = '\0';
    char *header_str = buffer;
    char *payload_str = pipe_pos + 1;

    cJSON *header = cJSON_Parse(header_str);
    if (!header) { printf("ERR: INVALID_ALG\n"); return 1; }

    cJSON *alg = cJSON_GetObjectItemCaseSensitive(header, "alg");
    if (!alg || !cJSON_IsString(alg) || strcmp(alg->valuestring, "none") != 0) {
        printf("ERR: INVALID_ALG\n");
        cJSON_Delete(header);
        return 1;
    }
    cJSON_Delete(header);

    cJSON *payload = cJSON_Parse(payload_str);
    if (!payload) { printf("ERR: MALFORMED_PAYLOAD\n"); return 2; }

    cJSON *user = cJSON_GetObjectItemCaseSensitive(payload, "user");
    cJSON *pin_hash = cJSON_GetObjectItemCaseSensitive(payload, "pin_hash");

    if (!user || !cJSON_IsString(user) || !pin_hash || !cJSON_IsNumber(pin_hash)) {
        printf("ERR: MALFORMED_PAYLOAD\n");
        cJSON_Delete(payload);
        return 2;
    }

    int target = pin_hash->valueint;
    for (int p = 0; p <= 9999; p++) {
        if ((p ^ 0x5A5A) == target) {
            printf("RECOVERED user=%s pin=%04d\n", user->valuestring, p);
            cJSON_Delete(payload);
            return 0;
        }
    }

    cJSON_Delete(payload);
    return 0;
}
EOF

# Temporarily fix cJSON to build the oracle, then break it again
sed -i 's/#include <strnig.h>/#include <string.h>/g' /app/cJSON-1.7.15/cJSON.c
gcc -c /app/cJSON-1.7.15/cJSON.c -o /app/cJSON.o
gcc /app/oracle.c /app/cJSON.o -I/app/cJSON-1.7.15 -o /app/oracle
sed -i 's/#include <string.h>/#include <strnig.h>/g' /app/cJSON-1.7.15/cJSON.c
rm /app/cJSON.o /app/oracle.c
chmod +x /app/oracle

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user