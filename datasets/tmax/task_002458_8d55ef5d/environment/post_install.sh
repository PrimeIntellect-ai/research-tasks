apt-get update && apt-get install -y python3 python3-pip gcc rustc expect
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/validator.c
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main() {
    char input[1024];
    printf("Enter route: ");
    fflush(stdout);
    if (!fgets(input, sizeof(input), stdin)) return 0;

    input[strcspn(input, "\n")] = 0;

    if (strncmp(input, "restore-", 8) != 0) {
        printf("[REJECTED]\n");
        return 0;
    }

    char *at_ptr = strchr(input, '@');
    if (!at_ptr) {
        printf("[REJECTED]\n");
        return 0;
    }
    char *second_at = strchr(at_ptr + 1, '@');
    if (second_at) {
        printf("[REJECTED]\n");
        return 0;
    }

    int local_len = at_ptr - (input + 8);
    if (local_len < 1) {
        printf("[REJECTED]\n");
        return 0;
    }
    for (int i = 8; i < 8 + local_len; i++) {
        if (!isalnum((unsigned char)input[i])) {
            printf("[REJECTED]\n");
            return 0;
        }
    }

    char *domain = at_ptr + 1;
    int domain_len = strlen(domain);
    if (domain_len < 9 || strcmp(domain + domain_len - 9, ".internal") != 0) {
        printf("[REJECTED]\n");
        return 0;
    }

    int mid_len = domain_len - 9;
    if (mid_len < 1) {
        printf("[REJECTED]\n");
        return 0;
    }
    for (int i = 0; i < mid_len; i++) {
        if (!islower((unsigned char)domain[i])) {
            printf("[REJECTED]\n");
            return 0;
        }
    }

    printf("[OK]\n");
    return 0;
}
EOF

    gcc -O2 /tmp/validator.c -o /app/validator
    strip /app/validator
    rm /tmp/validator.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user