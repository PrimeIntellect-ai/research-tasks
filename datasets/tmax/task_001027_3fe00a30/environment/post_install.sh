apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app

    # Generate the voicemail audio file
    espeak -w /app/voicemail.wav "Hey, it's the senior admin. We need that C differential manifest tool implemented ASAP. The program should read the old manifest from standard input, and read the new directory state from the file path provided as the first command-line argument. Each line in these files contains a file path, a tab character, and an integer checksum. You need to output the differences. Format each output line as the action—ADD, REMOVE, or MODIFY in all caps—followed by a colon, a space, and the file path. You must sort the final output alphabetically by the file path. Also, there are two strict edge cases: first, if any file path ends in dot tmp, completely ignore it. Do not add, remove, or modify it. Second, if a file in the new state has a checksum of exactly zero, you must treat it as a REMOVE action, regardless of whether it existed before. Get this done by today."

    # Create the oracle source code
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINES 5000
#define MAX_PATH 256

typedef struct {
    char path[MAX_PATH];
    unsigned int checksum;
} Entry;

typedef struct {
    char action[10];
    char path[MAX_PATH];
} Output;

Entry old_entries[MAX_LINES];
int old_count = 0;
Entry new_entries[MAX_LINES];
int new_count = 0;
Output outputs[MAX_LINES * 2];
int out_count = 0;

int compare_entries(const void *a, const void *b) {
    return strcmp(((Entry*)a)->path, ((Entry*)b)->path);
}

int compare_outputs(const void *a, const void *b) {
    return strcmp(((Output*)a)->path, ((Output*)b)->path);
}

int ends_with_tmp(const char *str) {
    size_t len = strlen(str);
    if (len >= 4 && strcmp(str + len - 4, ".tmp") == 0) return 1;
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;

    char line[512];
    while (fgets(line, sizeof(line), stdin)) {
        char path[MAX_PATH];
        unsigned int cs;
        if (sscanf(line, "%255[^\t]\t%u", path, &cs) == 2) {
            if (!ends_with_tmp(path)) {
                strcpy(old_entries[old_count].path, path);
                old_entries[old_count].checksum = cs;
                old_count++;
            }
        }
    }

    FILE *f = fopen(argv[1], "r");
    if (f) {
        while (fgets(line, sizeof(line), f)) {
            char path[MAX_PATH];
            unsigned int cs;
            if (sscanf(line, "%255[^\t]\t%u", path, &cs) == 2) {
                if (!ends_with_tmp(path)) {
                    strcpy(new_entries[new_count].path, path);
                    new_entries[new_count].checksum = cs;
                    new_count++;
                }
            }
        }
        fclose(f);
    }

    qsort(old_entries, old_count, sizeof(Entry), compare_entries);
    qsort(new_entries, new_count, sizeof(Entry), compare_entries);

    int i = 0, j = 0;
    while (i < old_count && j < new_count) {
        int cmp = strcmp(old_entries[i].path, new_entries[j].path);
        if (cmp < 0) {
            strcpy(outputs[out_count].action, "REMOVE");
            strcpy(outputs[out_count].path, old_entries[i].path);
            out_count++;
            i++;
        } else if (cmp > 0) {
            if (new_entries[j].checksum == 0) {
                strcpy(outputs[out_count].action, "REMOVE");
                strcpy(outputs[out_count].path, new_entries[j].path);
            } else {
                strcpy(outputs[out_count].action, "ADD");
                strcpy(outputs[out_count].path, new_entries[j].path);
            }
            out_count++;
            j++;
        } else {
            if (new_entries[j].checksum == 0) {
                strcpy(outputs[out_count].action, "REMOVE");
                strcpy(outputs[out_count].path, new_entries[j].path);
                out_count++;
            } else if (old_entries[i].checksum != new_entries[j].checksum) {
                strcpy(outputs[out_count].action, "MODIFY");
                strcpy(outputs[out_count].path, new_entries[j].path);
                out_count++;
            }
            i++;
            j++;
        }
    }

    while (i < old_count) {
        strcpy(outputs[out_count].action, "REMOVE");
        strcpy(outputs[out_count].path, old_entries[i].path);
        out_count++;
        i++;
    }

    while (j < new_count) {
        if (new_entries[j].checksum == 0) {
            strcpy(outputs[out_count].action, "REMOVE");
            strcpy(outputs[out_count].path, new_entries[j].path);
        } else {
            strcpy(outputs[out_count].action, "ADD");
            strcpy(outputs[out_count].path, new_entries[j].path);
        }
        out_count++;
        j++;
    }

    qsort(outputs, out_count, sizeof(Output), compare_outputs);

    for (int k = 0; k < out_count; k++) {
        // Handle deduplication if multiple REMOVEs happen
        if (k > 0 && strcmp(outputs[k].path, outputs[k-1].path) == 0) continue;
        printf("%s: %s\n", outputs[k].action, outputs[k].path);
    }

    return 0;
}
EOF

    # Compile the oracle program
    gcc -O2 /app/oracle.c -o /app/oracle_diff_tool
    rm /app/oracle.c

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user