apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        g++ \
        curl \
        wget \
        netcat \
        binutils \
        ltrace \
        strace \
        xxd

    pip3 install pytest flask requests

    mkdir -p /app

    # Create backend_api.py
    cat << 'EOF' > /app/backend_api.py
from flask import Flask, request
app = Flask(__name__)
@app.route('/flag')
def flag():
    if request.headers.get('X-Role') == 'admin':
        return "FLAG{bypass_successful_9921}"
    return "Access Denied", 403
if __name__ == '__main__':
    app.run(port=8081)
EOF

    # Create auth_gateway.cpp
    cat << 'EOF' > /app/auth_gateway.cpp
#include <iostream>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>
#include <sstream>

using namespace std;

string base64_decode(const string &in) {
    string out;
    vector<int> T(256, -1);
    for (int i=0; i<64; i++) T["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[i]] = i;
    int val=0, valb=-8;
    for (unsigned char c : in) {
        if (T[c] == -1) break;
        val = (val << 6) + T[c];
        valb += 6;
        if (valb >= 0) {
            out.push_back(char((val >> valb) & 0xFF));
            valb -= 8;
        }
    }
    return out;
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    while (true) {
        int new_socket = accept(server_fd, nullptr, nullptr);
        char buffer[4096] = {0};
        read(new_socket, buffer, 4096);
        string req(buffer);

        size_t auth_pos = req.find("Authorization: ");
        if (auth_pos != string::npos) {
            size_t end_pos = req.find("\r\n", auth_pos);
            string b64 = req.substr(auth_pos + 15, end_pos - auth_pos - 15);
            string decoded = base64_decode(b64);

            if (decoded.size() >= 41 && decoded.substr(0, 4) == "GATE") {
                char type = decoded[4];
                if (type == 0x00) {
                    // Vulnerability: skip HMAC, just check XOR checksum
                    uint16_t len = *(uint16_t*)(decoded.data() + 37);
                    if (decoded.size() >= 39 + len + 4) {
                        string payload = decoded.substr(39, len);
                        uint32_t checksum = *(uint32_t*)(decoded.data() + 39 + len);

                        uint32_t calc = 0;
                        for (size_t i = 0; i < payload.size(); i += 4) {
                            uint32_t chunk = 0;
                            for (size_t j = 0; j < 4; j++) {
                                if (i + j < payload.size()) {
                                    chunk |= (payload[i + j] << (j * 8));
                                }
                            }
                            calc ^= chunk;
                        }

                        if (calc == checksum && payload.find("role=admin") != string::npos) {
                            string resp = "HTTP/1.1 200 OK\r\n\r\nFLAG{bypass_successful_9921}\n";
                            send(new_socket, resp.c_str(), resp.length(), 0);
                            close(new_socket);
                            continue;
                        }
                    }
                }
            }
        }
        string resp = "HTTP/1.1 403 Forbidden\r\n\r\nAccess Denied\n";
        send(new_socket, resp.c_str(), resp.length(), 0);
        close(new_socket);
    }
    return 0;
}
EOF

    g++ -O3 /app/auth_gateway.cpp -o /app/auth_gateway
    rm /app/auth_gateway.cpp

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
python3 /app/backend_api.py &
/app/auth_gateway &
sleep 2
EOF
    chmod +x /app/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app