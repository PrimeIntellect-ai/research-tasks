apt-get update && apt-get install -y python3 python3-pip g++ imagemagick tesseract-ocr tcpdump
    pip3 install pytest scapy

    mkdir -p /app/src

    cat << 'EOF' > /app/src/server.cpp
#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
// Missing #include <pthread.h>

void* handle_client(void* arg) {
    int client_socket = *(int*)arg;
    delete (int*)arg;

    char buffer[2048];
    while (true) {
        memset(buffer, 0, sizeof(buffer));
        int bytes_read = read(client_socket, buffer, sizeof(buffer) - 1);
        if (bytes_read <= 0) break;

        // Memory leak
        char* leak_buffer = new char[1024];

        std::string request(buffer);
        size_t pipe_pos = request.find('|');
        if (pipe_pos == std::string::npos) {
            write(client_socket, "ERROR\n", 6);
            continue;
        }

        std::string auth_part = request.substr(0, pipe_pos);
        std::string data_part = request.substr(pipe_pos + 1);

        if (auth_part.find("AUTH X9K2-M4RQ-77AA") == std::string::npos) {
            write(client_socket, "AUTH_FAIL\n", 10);
            continue;
        }

        if (data_part.find("DATA ") == 0) {
            std::string payload = data_part.substr(5);
            // Crash defect
            if (payload.find("\x00\xff\xff\xff\xff") != std::string::npos) {
                char unsafe_buf[2];
                strcpy(unsafe_buf, payload.c_str()); // buffer overflow
            }
            write(client_socket, "OK\n", 3);
        } else {
            write(client_socket, "ERROR\n", 6);
        }
    }
    close(client_socket);
    return nullptr;
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));

    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(9000);

    bind(server_fd, (struct sockaddr*)&address, sizeof(address));
    listen(server_fd, 3);

    while (true) {
        int new_socket = accept(server_fd, nullptr, nullptr);
        pthread_t thread_id;
        int* client_sock = new int(new_socket);
        pthread_create(&thread_id, nullptr, handle_client, client_sock);
        pthread_detach(thread_id);
    }
    return 0;
}
EOF

    # Create the image
    convert -size 800x200 xc:white -pointsize 24 -fill black -draw "text 10,50 'The production authentication token is X9K2-M4RQ-77AA'" /app/auth_spec.png

    # Create the pcap
    cat << 'EOF' > /tmp/make_pcap.py
from scapy.all import *
pkts = []
ip = IP(dst="127.0.0.1", src="127.0.0.1")
tcp = TCP(sport=12345, dport=9000, flags="PA")
pkts.append(ip/tcp/Raw(load=b"AUTH X9K2-M4RQ-77AA|DATA Hello World\n"))
pkts.append(ip/tcp/Raw(load=b"AUTH X9K2-M4RQ-77AA|DATA \x00\xff\xff\xff\xff\n"))
wrpcap('/app/traffic.pcap', pkts)
EOF
    python3 /tmp/make_pcap.py
    rm /tmp/make_pcap.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app