apt-get update && apt-get install -y python3 python3-pip gcc g++ openssl libssl-dev wget curl binutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    cat << 'EOF' > /tmp/vuln.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[2048] = {0};

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8081);
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 10);

    while(1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if (new_socket < 0) continue;

        memset(buffer, 0, sizeof(buffer));
        read(new_socket, buffer, sizeof(buffer)-1);

        if (strstr(buffer, "GET /download") != NULL) {
            if (strstr(buffer, "Cookie: AdminSession=S3cr3tByp4ssM4st3r") != NULL) {
                char *file_param = strstr(buffer, "file=");
                if (file_param) {
                    file_param += 5;
                    char *end = strchr(file_param, ' ');
                    if (end) *end = '\0';
                    end = strchr(file_param, '&');
                    if (end) *end = '\0';

                    char filepath[512];
                    snprintf(filepath, sizeof(filepath), "uploads/%s", file_param);

                    FILE *f = fopen(filepath, "r");
                    if (f) {
                        char file_data[1024] = {0};
                        fread(file_data, 1, sizeof(file_data)-1, f);
                        fclose(f);
                        char response[2048];
                        snprintf(response, sizeof(response), "HTTP/1.1 200 OK\r\nContent-Length: %lu\r\n\r\n%s", strlen(file_data), file_data);
                        write(new_socket, response, strlen(response));
                    } else {
                        char *not_found = "HTTP/1.1 404 Not Found\r\n\r\n";
                        write(new_socket, not_found, strlen(not_found));
                    }
                } else {
                    char *bad_req = "HTTP/1.1 400 Bad Request\r\n\r\n";
                    write(new_socket, bad_req, strlen(bad_req));
                }
            } else {
                char *forbidden = "HTTP/1.1 403 Forbidden\r\n\r\n";
                write(new_socket, forbidden, strlen(forbidden));
            }
        } else {
            char *not_found = "HTTP/1.1 404 Not Found\r\n\r\n";
            write(new_socket, not_found, strlen(not_found));
        }
        close(new_socket);
    }
    return 0;
}
EOF

    gcc /tmp/vuln.c -o /app/vuln_uploader
    strip /app/vuln_uploader
    rm /tmp/vuln.c
    mkdir -p /app/uploads

    echo "FLAG{p4th_tr4v3rs4l_pr0xy}" > /home/user/flag.txt

    openssl req -x509 -newkey rsa:2048 -keyout /tmp/ca.key -out /home/user/ca.pem -days 365 -nodes -subj "/CN=TestCA"
    rm /tmp/ca.key

    chmod -R 777 /home/user