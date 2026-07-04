apt-get update && apt-get install -y python3 python3-pip openssh-client g++ gawk coreutils
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/.ssh

# Generate a temporary SSH key
ssh-keygen -t rsa -b 2048 -N "" -f /tmp/temp_key -q

# Prepare the JWT components
HEADER='{"alg":"HS256","typ":"JWT"}'
HEADER_B64=$(echo -n "$HEADER" | base64 -w 0 | tr '+/' '-_' | tr -d '=')

PAYLOAD=$(cat /tmp/temp_key)
PAYLOAD_B64=$(echo -n "$PAYLOAD" | base64 -w 0 | tr '+/' '-_' | tr -d '=')

SIGNATURE="fake_signature_for_hs256"

echo "${HEADER_B64}.${PAYLOAD_B64}.${SIGNATURE}" > /home/user/legacy_token.jwt

# Create the C++ extractor
cat << 'EOF' > /home/user/extractor.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

// Base64url decode helper (simplified for the task)
std::string base64_decode(const std::string& in) {
    std::string out;
    std::string b64 = in;
    for (char& c : b64) {
        if (c == '-') c = '+';
        if (c == '_') c = '/';
    }
    while (b64.length() % 4 != 0) b64 += '=';

    std::vector<int> T(256,-1);
    for(int i=0; i<64; i++) T["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[i]] = i; 

    int val=0, valb=-8;
    for(unsigned char c : b64) {
        if(T[c] == -1) break;
        val = (val<<6) + T[c];
        valb += 6;
        if(valb>=0) {
            out.push_back(char((val>>valb)&0xFF));
            valb-=8;
        }
    }
    return out;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <token_file>\n";
        return 1;
    }

    std::ifstream file(argv[1]);
    if (!file) return 1;
    std::string token;
    file >> token;

    size_t pos1 = token.find('.');
    size_t pos2 = token.find('.', pos1 + 1);

    if (pos1 == std::string::npos || pos2 == std::string::npos) {
        std::cerr << "Invalid JWT format\n";
        return 1;
    }

    std::string header_b64 = token.substr(0, pos1);
    std::string payload_b64 = token.substr(pos1 + 1, pos2 - pos1 - 1);
    std::string sig = token.substr(pos2 + 1);

    std::string header = base64_decode(header_b64);

    // VULNERABILITY: algorithm=none bypass
    bool is_valid = false;
    if (header.find("\"alg\":\"none\"") != std::string::npos || header.find("\"alg\": \"none\"") != std::string::npos) {
        is_valid = true;
    } else {
        // Mock HMAC verification that will always fail without the secret
        std::cerr << "HMAC validation failed. Secret required.\n";
        return 1;
    }

    if (is_valid) {
        std::cout << base64_decode(payload_b64) << std::endl;
    }

    return 0;
}
EOF

chmod -R 777 /home/user
chmod 700 /home/user/.ssh
chown -R user:user /home/user