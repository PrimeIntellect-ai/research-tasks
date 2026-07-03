apt-get update && apt-get install -y python3 python3-pip g++ iptables curl
    pip3 install pytest requests

    # Create /app directory and the legacy_auth binary
    mkdir -p /app
    cat << 'EOF' > /tmp/legacy_auth.cpp
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) return 1;
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) return 1;
    if (listen(server_fd, 10) < 0) return 1;
    while (true) {
        struct sockaddr_in client;
        socklen_t len = sizeof(client);
        int new_socket = accept(server_fd, (struct sockaddr *)&client, &len);
        if (new_socket >= 0) {
            char buffer[1024] = {0};
            read(new_socket, buffer, 1024);
            const char* response = "HTTP/1.1 200 OK\r\n\r\nAuthenticated";
            send(new_socket, response, strlen(response), 0);
            close(new_socket);
        }
    }
    return 0;
}
EOF
    g++ -O2 /tmp/legacy_auth.cpp -o /app/legacy_auth
    strip /app/legacy_auth
    rm /tmp/legacy_auth.cpp

    # Create /verify directory and the verifier script
    mkdir -p /verify
    cat << 'EOF' > /verify/run_eval.py
#!/usr/bin/env python3
import sys
# Placeholder for the actual evaluation logic
print("0.0")
EOF
    chmod +x /verify/run_eval.py

    # Create the user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user