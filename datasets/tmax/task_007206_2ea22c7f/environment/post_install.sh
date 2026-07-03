apt-get update && apt-get install -y python3 python3-pip gcc netcat
    pip3 install pytest

    mkdir -p /home/user/server
    cat << 'EOF' > /home/user/server/daemon.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

void sanitize(char *input) {
    char *pos;
    while ((pos = strstr(input, "<script>")) != NULL) {
        memset(pos, '_', 8);
    }
    while ((pos = strstr(input, "javascript:")) != NULL) {
        memset(pos, '_', 11);
    }
}

int calculate_token(const char *uri) {
    int sum = 0;
    for (int i = 0; i < strlen(uri); i++) {
        sum += uri[i];
    }
    return (sum % 256) ^ 0x42;
}

void handle_client(int client_sock) {
    char buffer[1024] = {0};
    read(client_sock, buffer, 1023);

    char method[16], uri[512], protocol[16];
    sscanf(buffer, "%15s %511s %15s", method, uri, protocol);

    char *token_header = strstr(buffer, "X-Auth-Token: ");
    if (!token_header) {
        char *resp = "HTTP/1.1 401 Unauthorized\r\n\r\nMissing Token\n";
        write(client_sock, resp, strlen(resp));
        close(client_sock);
        return;
    }

    int received_token;
    sscanf(token_header, "X-Auth-Token: %d", &received_token);

    if (received_token != calculate_token(uri)) {
        char *resp = "HTTP/1.1 403 Forbidden\r\n\r\nInvalid Token\n";
        write(client_sock, resp, strlen(resp));
        close(client_sock);
        return;
    }

    sanitize(uri);

    char response[2048];
    sprintf(response, "HTTP/1.1 200 OK\r\n"
                      "Content-Security-Policy: default-src 'none';\r\n"
                      "X-Reflected-Path: %s\r\n"
                      "Content-Length: 13\r\n\r\n"
                      "Hello, World!", uri);

    write(client_sock, response, strlen(response));
    close(client_sock);
}

int main() {
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_size;

    server_sock = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8888);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
    listen(server_sock, 5);

    while(1) {
        addr_size = sizeof(client_addr);
        client_sock = accept(server_sock, (struct sockaddr*)&client_addr, &addr_size);
        handle_client(client_sock);
    }
    return 0;
}
EOF

    gcc /home/user/server/daemon.c -o /home/user/server/daemon

    # Ensure the daemon starts when a shell is spawned
    echo "/home/user/server/daemon &" >> /etc/bash.bashrc
    echo "sleep 1" >> /etc/bash.bashrc

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user