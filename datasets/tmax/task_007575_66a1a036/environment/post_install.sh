apt-get update && apt-get install -y python3 python3-pip gcc openssl
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user

    cat << 'EOF' > /home/user/login_service.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Location: /secure/default\r\n\r\n");
        return 1;
    }
    char *next_param = argv[1];

    // Vulnerable: Open Redirect
    printf("Location: %s\r\n\r\n", next_param);
    return 0;
}
EOF

    cat << 'EOF' > /home/user/auth_logs.txt
[2023-10-01 10:00:00] 192.168.1.50 GET /login?next=/secure/dashboard HTTP/1.1 302
[2023-10-01 10:05:00] 10.0.0.5 GET /login?next=http://evil.com/login HTTP/1.1 302
[2023-10-01 10:07:00] 192.168.1.50 GET /login?next=/secure/profile HTTP/1.1 302
[2023-10-01 10:10:00] 172.16.0.4 GET /login?next=https://evil.com/malware HTTP/1.1 302
[2023-10-01 10:12:00] 10.0.0.5 GET /login?next=//evil.com/phish HTTP/1.1 302
[2023-10-01 10:15:00] 192.168.1.100 GET /login?next=/secure/settings HTTP/1.1 302
[2023-10-01 10:20:00] 10.9.8.7 GET /login?next=http://evil.com/drop HTTP/1.1 404
EOF

    openssl req -x509 -newkey rsa:2048 -keyout /home/user/suspicious.key -out /home/user/suspicious.crt -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Syndicate Hackers/CN=evil.com" 2>/dev/null
    rm /home/user/suspicious.key

    chown -R user:user /home/user
    chmod -R 777 /home/user