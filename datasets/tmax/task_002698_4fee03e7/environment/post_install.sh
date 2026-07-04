apt-get update && apt-get install -y python3 python3-pip gcc file
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/legacy_redactor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void replace_tls(char **str) {
    char *s = *str;
    char *begin;
    while ((begin = strstr(s, "-----BEGIN RSA PRIVATE KEY-----")) != NULL) {
        char *end = strstr(begin, "-----END RSA PRIVATE KEY-----");
        if (!end) break;
        end += strlen("-----END RSA PRIVATE KEY-----");

        size_t new_len = strlen(s) - (end - begin) + strlen("[REDACTED_TLS_KEY]");
        char *res = malloc(new_len + 1);
        size_t prefix_len = begin - s;
        strncpy(res, s, prefix_len);
        strcpy(res + prefix_len, "[REDACTED_TLS_KEY]");
        strcpy(res + prefix_len + strlen("[REDACTED_TLS_KEY]"), end);

        free(s);
        s = res;
    }
    *str = s;
}

void replace_creds(char **str, const char *prefix) {
    char *s = *str;
    char *pos;
    while ((pos = strstr(s, prefix)) != NULL) {
        char *val_start = pos + strlen(prefix);
        char *val_end = val_start;
        while (*val_end && !isspace((unsigned char)*val_end)) {
            val_end++;
        }

        size_t new_len = strlen(s) - (val_end - val_start) + 3;
        char *res = malloc(new_len + 1);
        size_t prefix_len = pos - s + strlen(prefix);
        strncpy(res, s, prefix_len);
        strcpy(res + prefix_len, "***");
        strcpy(res + prefix_len + 3, val_end);

        free(s);
        s = res;
    }
    *str = s;
}

int main() {
    char *buffer = malloc(1000000);
    if (!buffer) return 1;
    size_t len = fread(buffer, 1, 999999, stdin);
    buffer[len] = '\0';

    replace_tls(&buffer);
    replace_creds(&buffer, "password=");
    replace_creds(&buffer, "token=");

    if (strstr(buffer, "sudo su") || strstr(buffer, "chmod +s")) {
        printf("[ALERT-CWE-269] ");
    }
    printf("%s", buffer);
    free(buffer);
    return 0;
}
EOF

    gcc -O2 /tmp/legacy_redactor.c -o /app/legacy_redactor
    strip -s /app/legacy_redactor
    chmod +x /app/legacy_redactor
    rm /tmp/legacy_redactor.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user