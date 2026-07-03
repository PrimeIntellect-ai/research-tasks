apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        g++ \
        libssl-dev \
        nlohmann-json3-dev \
        binutils \
        strace \
        ltrace \
        xxd

    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <poll.h>
#include <openssl/sha.h>
#include <iomanip>
#include <sstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

std::map<std::string, std::string> config;
std::string filename;

void load_config() {
    config.clear();
    int fd = open(filename.c_str(), O_RDONLY);
    if (fd < 0) return;
    struct stat sb;
    if (fstat(fd, &sb) < 0 || sb.st_size < 4) { close(fd); return; }
    char* data = (char*)mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (data == MAP_FAILED) { close(fd); return; }

    if (std::string(data, 4) == "CFG1") {
        size_t pos = 4;
        while (pos + 2 <= sb.st_size) {
            uint16_t klen = *(uint16_t*)(data + pos);
            pos += 2;
            if (pos + klen > sb.st_size) break;
            std::string key(data + pos, klen);
            pos += klen;
            if (pos + 4 > sb.st_size) break;
            uint32_t vlen = *(uint32_t*)(data + pos);
            pos += 4;
            if (pos + vlen > sb.st_size) break;
            std::string val(data + pos, vlen);
            pos += vlen;
            config[key] = val;
        }
    }
    munmap(data, sb.st_size);
    close(fd);
}

void print_hash() {
    std::string buffer;
    for (auto const& [k, v] : config) {
        buffer += k + "=" + v + "\n";
    }
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char*)buffer.c_str(), buffer.length(), hash);
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    std::cout << std::endl;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    filename = argv[1];

    load_config();

    int inotify_fd = inotify_init1(IN_NONBLOCK);
    int wd = inotify_add_watch(inotify_fd, filename.c_str(), IN_MODIFY);

    struct pollfd pfd[2];
    pfd[0].fd = STDIN_FILENO;
    pfd[0].events = POLLIN;
    pfd[1].fd = inotify_fd;
    pfd[1].events = POLLIN;

    std::string line;
    while (true) {
        int ret = poll(pfd, 2, -1);
        if (ret < 0) break;

        if (pfd[1].revents & POLLIN) {
            char buf[4096] __attribute__ ((aligned(__alignof__(struct inotify_event))));
            ssize_t len = read(inotify_fd, buf, sizeof(buf));
            if (len > 0) {
                load_config();
                print_hash();
            }
        }

        if (pfd[0].revents & POLLIN) {
            if (!std::getline(std::cin, line)) break;
            try {
                auto j = json::parse(line);
                std::string op = j.value("op", "");
                if (op == "PUT") {
                    config[j.value("k", "")] = j.value("v", "");
                } else if (op == "DEL") {
                    config.erase(j.value("k", ""));
                }
                print_hash();
            } catch (...) {
                // ignore malformed
            }
        }
    }
    return 0;
}
EOF

    g++ -O3 -std=c++17 /tmp/oracle.cpp -o /app/legacy_config_tracker -lcrypto
    strip /app/legacy_config_tracker
    rm /tmp/oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user