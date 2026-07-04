apt-get update && apt-get install -y python3 python3-pip g++ make git netcat-openbsd
    pip3 install pytest

    mkdir -p /app/vendored_kv /app/data
    cd /app/vendored_kv

    git config --global user.email "test@example.com"
    git config --global user.name "Test User"
    git config --global init.defaultBranch main
    git init

    cat << 'EOF' > server.cpp
#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>

std::unordered_map<std::string, std::string> db;
std::string expected_token;

void load_wal(const std::string& path) {
    std::ifstream file(path);
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int seq; std::string op, key, val;
        if (!(iss >> seq >> op >> key >> val)) {
            std::cerr << "WAL corruption detected on line: " << line << std::endl;
            abort();
        }
        if (op == "SET") db[key] = val;
    }
}

void handle_client(int client_fd) {
    char buffer[1024];
    bool authenticated = false;
    while (true) {
        memset(buffer, 0, 1024);
        int bytes_read = read(client_fd, buffer, 1023);
        if (bytes_read <= 0) break;

        std::istringstream iss(buffer);
        std::string cmd;
        iss >> cmd;

        if (cmd == "AUTH") {
            std::string token;
            iss >> token;
            if (token == expected_token) {
                authenticated = true;
                send(client_fd, "OK\n", 3, 0);
            } else {
                send(client_fd, "ERR\n", 4, 0);
            }
        } else if (cmd == "GET" && authenticated) {
            std::string key;
            iss >> key;
            char* response = new char[1024]; // MEMORY LEAK HERE
            if (db.count(key)) {
                snprintf(response, 1024, "VALUE %s\n", db[key].c_str());
            } else {
                snprintf(response, 1024, "NOT_FOUND\n");
            }
            send(client_fd, response, strlen(response), 0);
        } else if (cmd == "SET" && authenticated) {
            std::string key, val;
            iss >> key >> val;
            db[key] = val;
            send(client_fd, "OK\n", 3, 0);
        }
    }
    close(client_fd);
}

int main(int argc, char** argv) {
    if (argc < 3) return 1;
    load_wal(argv[1]);

    // Read token from env for prod, fallback for dev
    const char* env_tok = getenv("AUTH_TOKEN");
    expected_token = env_tok ? env_tok : "b34r3r_s3cr3t";

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));

    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(std::stoi(argv[2]));

    bind(server_fd, (struct sockaddr*)&address, sizeof(address));
    listen(server_fd, 3);

    while (true) {
        int client_fd = accept(server_fd, nullptr, nullptr);
        std::thread(handle_client, client_fd).detach();
    }
    return 0;
}
EOF

    cat << 'EOF' > Makefile
CXX = g++
CXXFLAGS = -Wall -std=c++14

kv_server: server.cpp
	$(CXX) $(CXXFLAGS) -o kv_server server.cpp
EOF

    git add server.cpp Makefile
    git commit -m "Initial commit with AUTH_TOKEN b34r3r_s3cr3t built-in"

    sed -i 's/expected_token = env_tok ? env_tok : "b34r3r_s3cr3t";/expected_token = env_tok ? env_tok : "dev_token";/g' server.cpp
    git commit -am "Security refactor: Remove hardcoded admin token"

    cat << 'EOF' > /app/data/server.wal
1 SET app_name kv_server
2 SET version 1.0
3 SET uptime 999
4 SET corrupted_key
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app