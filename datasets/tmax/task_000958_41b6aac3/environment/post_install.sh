apt-get update && apt-get install -y python3 python3-pip gcc nginx socat expect acl sudo curl
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    useradd -m -s /bin/bash guest || true

    mkdir -p /home/user/app/nginx /home/user/app/private

    cat << 'EOF' > /home/user/app/nginx/nginx.conf
events { worker_connections 1024; }
http {
    server {
        listen 8080;
        location /send {
            proxy_pass http://unix:/home/user/app/private/wrong.sock;
        }
    }
}
EOF

    cat << 'EOF' > /home/user/app/oracle_sanitize.c
#include <stdio.h>
#include <ctype.h>
int main() {
    int c;
    while ((c = getchar()) != EOF) {
        if (isalnum(c) || c == ' ') {
            putchar(toupper(c));
        }
    }
    return 0;
}
EOF
    gcc -O2 /home/user/app/oracle_sanitize.c -o /home/user/app/oracle_sanitize

    chmod -R 777 /home/user
    chmod 700 /home/user/app/private