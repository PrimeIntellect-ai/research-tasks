apt-get update && apt-get install -y python3 python3-pip g++ binutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/login.cpp
#include <iostream>
#include <string>

void handle_login(std::string username, std::string password, std::string redirect_url) {
    bool authenticated = check_credentials(username, password);
    if (authenticated) {
        // Log the user in
        std::cout << "HTTP/1.1 302 Found\n";
        // Vulnerable to Open Redirect (CWE-601)
        std::cout << "Location: " << redirect_url << "\n\n";
    } else {
        std::cout << "HTTP/1.1 401 Unauthorized\n\n";
    }
}
EOF

    cat << 'EOF' > /home/user/legacy_auth.cpp
#include <iostream>
#include <cstring>

int check_password(const char* p) {
    if (strlen(p) != 5) return 0;
    if ((p[0]^0x42) == 0x23 && 
        (p[1]^0x42) == 0x26 && 
        (p[2]^0x42) == 0x2f && 
        (p[3]^0x42) == 0x2b && 
        (p[4]^0x42) == 0x2c) {
        return 1;
    }
    return 0;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    if (check_password(argv[1])) {
        std::cout << "Access Granted\n";
        return 0;
    }
    std::cout << "Access Denied\n";
    return 1;
}
EOF

    g++ -O0 /home/user/legacy_auth.cpp -o /home/user/legacy_auth
    strip /home/user/legacy_auth
    rm /home/user/legacy_auth.cpp

    chmod -R 777 /home/user