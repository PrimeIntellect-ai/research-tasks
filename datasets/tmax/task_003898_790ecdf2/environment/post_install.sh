apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/logs

    cat << 'EOF' > /home/user/logs/service_A.log
ID:A1|TS:1670000000|MSG:Initialization started
ID:A2|TS:1670000010|MSG:Process running normally
EOF

    cat << 'EOF' > /home/user/logs/service_B.log
ID:B1|TS:1670000005|MSG:Authentication successful
ID:B2|TS:1670000008|MSG:User naïve logged in
ID:B3|TS:1670000015|MSG:Session closed
EOF

    cat << 'EOF' > /home/user/merge_logs.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

typedef struct {
    char id[16];
    long ts;
    char msg[256];
} LogEntry;

// BUG: signed char comparison causes UTF-8 characters (which have the high bit set) 
// to evaluate as < 0, prematurely terminating the length calculation.
int calculate_msg_len(const char* msg) {
    int len = 0;
    while (msg[len] != '\0' && msg[len] != '\n') {
        if (msg[len] < 0) { // Bug is here
            break;
        }
        len++;
    }
    return len;
}

int main() {
    DIR *dir;
    struct dirent *ent;
    LogEntry entries[100];
    int count = 0;

    if ((dir = opendir("/home/user/logs")) != NULL) {
        while ((ent = readdir(dir)) != NULL) {
            if (strstr(ent->d_name, ".log")) {
                char filepath[512];
                sprintf(filepath, "/home/user/logs/%s", ent->d_name);
                FILE *f = fopen(filepath, "r");
                char line[512];
                while (fgets(line, sizeof(line), f)) {
                    char *id_ptr = strstr(line, "ID:");
                    char *ts_ptr = strstr(line, "TS:");
                    char *msg_ptr = strstr(line, "MSG:");

                    if (id_ptr && ts_ptr && msg_ptr) {
                        sscanf(id_ptr, "ID:%15[^|]", entries[count].id);
                        sscanf(ts_ptr, "TS:%ld", &entries[count].ts);

                        msg_ptr += 4; // skip "MSG:"
                        int msg_len = calculate_msg_len(msg_ptr);
                        strncpy(entries[count].msg, msg_ptr, msg_len);
                        entries[count].msg[msg_len] = '\0';
                        count++;
                    }
                }
                fclose(f);
            }
        }
        closedir(dir);
    }

    // Simple bubble sort by timestamp
    for (int i = 0; i < count - 1; i++) {
        for (int j = 0; j < count - i - 1; j++) {
            if (entries[j].ts > entries[j+1].ts) {
                LogEntry temp = entries[j];
                entries[j] = entries[j+1];
                entries[j+1] = temp;
            }
        }
    }

    FILE *out = fopen("/home/user/merged.out", "w");
    for (int i = 0; i < count; i++) {
        fprintf(out, "[%ld] %s - %s\n", entries[i].ts, entries[i].id, entries[i].msg);
    }
    fclose(out);

    return 0;
}
EOF

    chmod -R 777 /home/user