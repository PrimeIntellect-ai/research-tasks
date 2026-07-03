apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/rotator.c
#include <stdio.h>
#include <string.h>

struct AuthContext {
    char decoded_cookie[64];
    unsigned int isAdmin;
};

void hex_decode(const char *src, char *dst) {
    while (*src && src[1]) {
        sscanf(src, "%2hhx", dst);
        src += 2;
        dst++;
    }
    *dst = '\0';
}

void rotate_credentials() {
    FILE *f = fopen("/home/user/rotated_password.txt", "w");
    if (f) {
        fprintf(f, "ROTATED_OK_7739\n");
        fclose(f);
        printf("Credentials rotated successfully.\n");
    }
}

int main() {
    char buffer[1024] = {0};
    struct AuthContext ctx;
    ctx.isAdmin = 0;
    char cookie_val[256] = {0};

    // Read raw HTTP request from stdin
    fread(buffer, 1, sizeof(buffer)-1, stdin);

    // Look for Cookie header
    char *cookie_ptr = strstr(buffer, "Cookie: session=");
    if (cookie_ptr) {
        sscanf(cookie_ptr, "Cookie: session=%255s", cookie_val);
        // Vulnerable hex decode - reads up to 255 chars, decodes into 64-byte buffer
        hex_decode(cookie_val, ctx.decoded_cookie); 

        if (ctx.isAdmin == 0xdeadbeef) {
            rotate_credentials();
        } else {
            printf("Access denied.\n");
        }
    }
    return 0;
}
EOF

    gcc /home/user/rotator.c -o /home/user/rotator

    chmod -R 777 /home/user