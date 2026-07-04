apt-get update && apt-get install -y python3 python3-pip gcc make binutils
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /tmp/server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

void handle_client(int client_sock) {
    unsigned char header[8];
    while (1) {
        int n = recv(client_sock, header, 8, MSG_WAITALL);
        if (n <= 0) break;
        if (header[0] != 0x53 || header[1] != 0x45 || header[2] != 0x43 || header[3] != 0x55) break;

        unsigned short cmd = (header[4] << 8) | header[5];
        unsigned short len = (header[6] << 8) | header[7];

        unsigned char payload[1024];
        if (len > 0) {
            n = recv(client_sock, payload, len, MSG_WAITALL);
            if (n <= 0) break;
        }

        if (cmd == 1) {
            unsigned char resp[12] = {0x53, 0x45, 0x43, 0x55, 0x00, 0x01, 0x00, 0x04, 'P', 'O', 'N', 'G'};
            send(client_sock, resp, 12, 0);
        } else if (cmd == 2) {
            if (len == 15 && memcmp(payload, "secret_token_99", 15) == 0) {
                unsigned char resp[10] = {0x53, 0x45, 0x43, 0x55, 0x00, 0x02, 0x00, 0x02, 'O', 'K'};
                send(client_sock, resp, 10, 0);
            } else {
                unsigned char resp[10] = {0x53, 0x45, 0x43, 0x55, 0x00, 0x02, 0x00, 0x02, 'N', 'O'};
                send(client_sock, resp, 10, 0);
            }
        } else if (cmd == 3) {
            char buf[64];
            payload[len] = '\0';
            strcpy(buf, (char*)payload);

            unsigned char resp[10] = {0x53, 0x45, 0x43, 0x55, 0x00, 0x03, 0x00, 0x02, 'O', 'K'};
            send(client_sock, resp, 10, 0);
        } else {
            break;
        }
    }
    close(client_sock);
}

int main() {
    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(8000);

    bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
    listen(server_sock, 5);

    while (1) {
        int client_sock = accept(server_sock, NULL, NULL);
        if (client_sock >= 0) {
            if (fork() == 0) {
                close(server_sock);
                handle_client(client_sock);
                exit(0);
            }
            close(client_sock);
        }
    }
    return 0;
}
EOF

    gcc -O0 -fno-stack-protector -o /app/suspicious_service /tmp/server.c
    strip /app/suspicious_service
    rm /tmp/server.c

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/fuzzer

    cat << 'EOF' > /home/user/fuzzer/harness.c
#include <stdio.h>
#include <arpa/inets.h>

int main() {
    int unused_var = 0;
    printf("Harness ready.\n");
    return 0;
}
EOF

    cat << 'EOF' > /home/user/fuzzer/Makefile
CC = gcc
CFLAGS = -Wall -Werror

harness: harness.c
	$(CC) $(CFLAGS) -o harness harness.c
EOF

    chown -R user:user /home/user
    chmod -R 777 /home/user