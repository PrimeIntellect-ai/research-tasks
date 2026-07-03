apt-get update && apt-get install -y python3 python3-pip g++
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'EOF' > /home/user/server.cpp
#include <iostream>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    const char* flag = "FLAG{m3m0ry_l34k_r3c0v3ry_9921}";
    const char* messages[] = {
        "Welcome",
        "Status: OK",
        "System idle"
    };
    // The flag is conceptually adjacent in memory for this simplified challenge, 
    // but to guarantee memory layout across compilers, we simulate the OOB read conceptually:
    const char* memory_layout[] = {
        messages[0],
        messages[1],
        messages[2],
        flag
    };

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) return 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) return 1;

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(9999);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) return 1;
    if (listen(server_fd, 3) < 0) return 1;

    while (true) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) continue;

        unsigned char buffer[2] = {0};
        read(new_socket, buffer, 2);

        // buffer[0] is command (1 = read message)
        // buffer[1] is index
        if (buffer[0] == 1) {
            // Vulnerability: No bounds checking on index (CWE-125)
            // Valid indices are 0, 1, 2. Index 3 leaks the flag.
            unsigned char index = buffer[1];
            if (index <= 3) { // Simulate up to index 3 being readable in this bounded layout
                send(new_socket, memory_layout[index], strlen(memory_layout[index]), 0);
            } else {
                send(new_socket, "SEGFAULT", 8, 0);
            }
        }
        close(new_socket);
    }
    return 0;
}
EOF

g++ /home/user/server.cpp -o /home/user/server

cat << 'EOF' > /home/user/ids.log
[2023-10-24 10:15:01] [10.0.0.5] [01 00]
[2023-10-24 10:16:22] [192.168.1.50] [01 01]
[2023-10-24 10:18:45] [10.0.0.5] [01 02]
[2023-10-24 10:22:11] [172.16.20.100] [02 00]
[2023-10-24 10:25:33] [198.51.100.42] [01 03]
[2023-10-24 10:30:00] [10.0.0.5] [01 00]
EOF

# Ensure the server starts when an interactive shell is spawned
echo "/home/user/server &" >> /home/user/.bashrc

chmod -R 777 /home/user