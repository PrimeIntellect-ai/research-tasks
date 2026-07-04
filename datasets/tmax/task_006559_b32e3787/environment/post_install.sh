apt-get update && apt-get install -y python3 python3-pip gcc build-essential
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/server.log
10.0.0.5 - - [10/Oct/2023:10:00:00] "GET /api/user_data?token=dGVzdDp1c2Vy HTTP/1.1" 200 120
10.0.0.6 - - [10/Oct/2023:10:05:00] "GET /api/admin_panel?token=YmFkZ3V5OmludHJ1ZGVyAAAAAAAAAAAAAAAAAAAAAAAB HTTP/1.1" 200 500
10.0.0.7 - - [10/Oct/2023:10:10:00] "GET /api/admin_panel?token=Z29vZDp1c2Vy HTTP/1.1" 403 120
EOF

    cat << 'EOF' > /home/user/token_validator.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void validate_token(const char* token) {
    int is_admin = 0;
    char buffer[32];

    // Vulnerability: strcpy doesn't check bounds, allowing overflow into is_admin
    strcpy(buffer, token);

    if (is_admin) {
        printf("Access Granted: Admin\n");
    } else {
        printf("Access Granted: User\n");
    }
}

int main(int argc, char** argv) {
    if(argc > 1) {
        validate_token(argv[1]);
    }
    return 0;
}
EOF

    chmod -R 777 /home/user