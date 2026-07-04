apt-get update && apt-get install -y python3 python3-pip g++ xxd
pip3 install pytest

mkdir -p /home/user
cd /home/user

# Generate a random secret token
SECRET_TOKEN=$(head -c 16 /dev/urandom | xxd -p)
echo -n "$SECRET_TOKEN" > /home/user/secret.txt

# Create the vulnerable C++ source code
cat << 'EOF' > /home/user/vault.cpp
#include <iostream>
#include <fstream>
#include <string.h>
#include <vector>

struct AuthContext {
    char password[16];
    int isAuthenticated;
};

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <password> <file_to_decrypt>\n";
        return 1;
    }

    AuthContext ctx;
    ctx.isAuthenticated = 0;

    // VULNERABILITY: Buffer overflow
    strcpy(ctx.password, argv[1]);

    if (strcmp(ctx.password, "Sup3rS3cr3tP@ss") == 0) {
        ctx.isAuthenticated = 1;
    }

    if (ctx.isAuthenticated != 0) {
        std::ifstream inFile(argv[2], std::ios::binary);
        if (!inFile) {
            std::cerr << "Failed to open file.\n";
            return 1;
        }
        std::vector<char> buffer((std::istreambuf_iterator<char>(inFile)), std::istreambuf_iterator<char>());

        // Simple XOR decryption with key 0x5A for demonstration
        for (size_t i = 0; i < buffer.size(); ++i) {
            buffer[i] ^= 0x5A;
        }

        std::cout << std::string(buffer.begin(), buffer.end());
    } else {
        std::cerr << "Access Denied.\n";
        return 1;
    }

    return 0;
}
EOF

# Compile the vulnerable program
g++ -fno-stack-protector -O0 /home/user/vault.cpp -o /home/user/vault

# Encrypt the secret token
cat << 'EOF' > /home/user/encrypt.cpp
#include <iostream>
#include <fstream>
#include <vector>

int main(int argc, char* argv[]) {
    std::ifstream inFile(argv[1], std::ios::binary);
    std::vector<char> buffer((std::istreambuf_iterator<char>(inFile)), std::istreambuf_iterator<char>());
    for (size_t i = 0; i < buffer.size(); ++i) {
        buffer[i] ^= 0x5A;
    }
    std::ofstream outFile(argv[2], std::ios::binary);
    outFile.write(buffer.data(), buffer.size());
    return 0;
}
EOF
g++ /home/user/encrypt.cpp -o /home/user/encrypt
/home/user/encrypt /home/user/secret.txt /home/user/confidential.enc
rm /home/user/encrypt.cpp /home/user/encrypt /home/user/secret.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user