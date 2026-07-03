apt-get update && apt-get install -y python3 python3-pip gcc make wget tar
    pip3 install pytest

    mkdir -p /app/vendor
    cd /app/vendor
    wget -qO cjson.tar.gz https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.tar.gz
    tar -xzf cjson.tar.gz
    mv cJSON-1.7.15 cJSON
    rm cjson.tar.gz

    # Mutate the Makefile to remove -fPIC
    sed -i 's/-fPIC//g' /app/vendor/cJSON/Makefile

    mkdir -p /app/oracle
    cat << 'EOF' > /app/oracle/log_converter_oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include "cJSON.h"

#pragma pack(push, 1)
struct LogEntry {
    uint32_t timestamp;
    uint8_t level;
    char message[64];
};
#pragma pack(pop)

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) return 1;

    struct flock fl;
    fl.l_type = F_RDLCK;
    fl.l_whence = SEEK_SET;
    fl.l_start = 0;
    fl.l_len = 0;
    fcntl(fd, F_SETLKW, &fl);

    cJSON *array = cJSON_CreateArray();
    struct LogEntry entry;
    while (read(fd, &entry, sizeof(entry)) == sizeof(entry)) {
        cJSON *obj = cJSON_CreateObject();
        cJSON_AddNumberToObject(obj, "time", entry.timestamp);
        cJSON_AddNumberToObject(obj, "lvl", entry.level);
        cJSON_AddStringToObject(obj, "msg", entry.message);
        cJSON_AddItemToArray(array, obj);
    }

    fl.l_type = F_UNLCK;
    fcntl(fd, F_SETLK, &fl);
    close(fd);

    char *json = cJSON_PrintUnformatted(array);
    printf("%s\n", json);
    free(json);
    cJSON_Delete(array);

    return 0;
}
EOF

    cd /app/oracle
    gcc -O2 -I/app/vendor/cJSON log_converter_oracle.c /app/vendor/cJSON/cJSON.c -o log_converter_oracle
    chmod +x log_converter_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user