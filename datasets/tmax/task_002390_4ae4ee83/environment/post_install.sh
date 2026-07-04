apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /app
    mkdir -p /etc/creds
    mkdir -p /verify/corpus/evil
    mkdir -p /verify/corpus/clean

    cat << 'EOF' > /app/cred_rotator.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void urldecode(char *dst, const char *src) {
    char a, b;
    while (*src) {
        if ((*src == '%') &&
            ((a = src[1]) && (b = src[2])) &&
            (isxdigit(a) && isxdigit(b))) {
            if (a >= 'a') a -= 'a'-'A';
            if (a >= 'A') a -= ('A' - 10);
            else a -= '0';
            if (b >= 'a') b -= 'a'-'A';
            if (b >= 'A') b -= ('A' - 10);
            else b -= '0';
            *dst++ = 16*a+b;
            src+=3;
        } else if (*src == '+') {
            *dst++ = ' ';
            src++;
        } else {
            *dst++ = *src++;
        }
    }
    *dst = '\0';
}

void process_request(const char *header_val) {
    char decoded[1024];
    urldecode(decoded, header_val);

    if (strstr(decoded, "../") != NULL) {
        return;
    }

    for (int i = 0; decoded[i]; i++) {
        if (decoded[i] == '\\') {
            decoded[i] = '/';
        }
    }

    char final_path[2048];
    snprintf(final_path, sizeof(final_path), "/etc/creds/%s", decoded);
    FILE *f = fopen(final_path, "w");
    if (f) fclose(f);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        process_request(argv[1]);
    }
    return 0;
}
EOF

    gcc -O2 /app/cred_rotator.c -o /app/cred_rotator
    strip /app/cred_rotator
    rm /app/cred_rotator.c

    cat << 'EOF' > /verify/corpus/evil/req1.txt
POST /rotate HTTP/1.1
Host: localhost
X-Cred-Path: service\..\..\etc\passwd
Content-Length: 0

EOF

    cat << 'EOF' > /verify/corpus/evil/req2.txt
POST /rotate HTTP/1.1
Host: localhost
X-Cred-Path: %2e%2e%5csecret
Content-Length: 0

EOF

    cat << 'EOF' > /verify/corpus/clean/req1.txt
POST /rotate HTTP/1.1
Host: localhost
X-Cred-Path: service_a/db_pass.txt
Content-Length: 0

EOF

    cat << 'EOF' > /verify/corpus/clean/req2.txt
POST /rotate HTTP/1.1
Host: localhost
X-Cred-Path: %61%64%6d%69%6e%2f%70%61%73%73
Content-Length: 0

EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user