apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create traffic.log
    cat << 'EOF' > /home/user/traffic.log
GET /api/v1/data HTTP/1.1
Host: internal-service.local
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidmlld2VyIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
User-Agent: curl/7.68.0
Accept: */*
EOF

    # Create and compile auth_checker
    cat << 'EOF' > /home/user/auth_checker.c
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    // Hidden role string inside the binary
    const char* hidden_role = "super_administrator_992";

    if (argc < 2) {
        printf("Usage: %s <jwt_token>\n", argv[0]);
        return 1;
    }

    char *token = argv[1];

    // Check if header contains alg: none (eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0)
    // Check if payload contains user: admin and role: super_administrator_992 (eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoic3VwZXJfYWRtaW5pc3RyYXRvcl85OTIifQ)
    if (strstr(token, "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0") != NULL &&
        strstr(token, "eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoic3VwZXJfYWRtaW5pc3RyYXRvcl85OTIifQ") != NULL) {
        // Signature part should be empty, token ends with a dot
        if (token[strlen(token)-1] == '.') {
            printf("FLAG{alg_none_bypass_success_8812}\n");
            return 0;
        }
    }

    printf("Access Denied: Invalid Signature or Claims\n");
    return 1;
}
EOF

    gcc -o /home/user/auth_checker /home/user/auth_checker.c
    rm /home/user/auth_checker.c

    chmod -R 777 /home/user