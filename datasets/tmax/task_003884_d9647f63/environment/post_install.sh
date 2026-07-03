apt-get update && apt-get install -y python3 python3-pip gcc make nginx curl
    pip3 install pytest

    mkdir -p /home/user/iot_pipeline/src
    mkdir -p /home/user/iot_pipeline/nginx
    mkdir -p /home/user/corpora/clean
    mkdir -p /home/user/corpora/evil

    cat << 'EOF' > /home/user/iot_pipeline/nginx/nginx.conf
events {}
http {
    server {
        listen 8080;
        location /ingest {
            proxy_pass http://127.0.0.1:9000;
        }
    }
}
EOF

    cat << 'EOF' > /home/user/iot_pipeline/src/daemon.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

extern int validate_payload(const unsigned char *data, size_t len);

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[4096] = {0};

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8081);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    while(1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }

        int valread = read(new_socket, buffer, 4096);
        if (valread > 0) {
            char *body = strstr(buffer, "\r\n\r\n");
            if (body) {
                body += 4;
                int body_len = valread - (body - buffer);
                int is_valid = validate_payload((unsigned char*)body, body_len);
                char *response;
                if (is_valid) {
                    response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK";
                } else {
                    response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 3\r\n\r\nBAD";
                }
                write(new_socket, response, strlen(response));
            }
        }
        close(new_socket);
    }
    return 0;
}
EOF

    cat << 'EOF' > /home/user/iot_pipeline/src/payload_filter.c
#include <stddef.h>

int validate_payload(const unsigned char *data, size_t len) {
    return 1;
}
EOF

    cat << 'EOF' > /home/user/iot_pipeline/src/Makefile
CC = gcc
CFLAGS = -Wall -fPIC
LDFLAGS = -shared

all: libpayload.so daemon

libpayload.so: payload_filter.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o libpayload.so payload_filter.c

daemon: daemon.c libpayload.so
	$(CC) -Wall -o daemon daemon.c -L. -lpayload

clean:
	rm -f libpayload.so daemon
EOF

    cat << 'EOF' > /home/user/iot_pipeline/start_services.sh
#!/bin/bash
cd /home/user/iot_pipeline/src
make clean && make
./daemon &
DAEMON_PID=$!
nginx -c /home/user/iot_pipeline/nginx/nginx.conf -g "daemon off;" &
NGINX_PID=$!
wait $DAEMON_PID $NGINX_PID
EOF
    chmod +x /home/user/iot_pipeline/start_services.sh

    python3 -c '
import os
import struct

def make_clean(path, length):
    magic = 0xDEADBEEF
    with open(path, "wb") as f:
        f.write(struct.pack(">I", magic))
        f.write(struct.pack(">I", length))
        f.write(os.urandom(length))

def make_evil(path, magic, length, real_length):
    with open(path, "wb") as f:
        f.write(struct.pack(">I", magic))
        f.write(struct.pack(">I", length))
        f.write(os.urandom(real_length))

make_clean("/home/user/corpora/clean/clean1.bin", 10)
make_clean("/home/user/corpora/clean/clean2.bin", 20)
make_evil("/home/user/corpora/evil/evil1.bin", 0xDEADBEEF, 10, 5)
make_evil("/home/user/corpora/evil/evil2.bin", 0xBAADF00D, 10, 10)
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user