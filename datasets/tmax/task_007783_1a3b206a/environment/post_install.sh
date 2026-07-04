apt-get update && apt-get install -y python3 python3-pip libssl-dev g++ binutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/uploads

    cat << 'EOF' > /tmp/upload_agent.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <openssl/evp.h>
#include <openssl/aes.h>

const unsigned char aes_key[] = "Sup3rS3cr3tK3y!!";
const unsigned char aes_iv[]  = "1n1t1alV3ct0r123";

int decrypt(const std::vector<unsigned char>& ciphertext, std::vector<unsigned char>& plaintext) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int len;
    int plaintext_len;

    plaintext.resize(ciphertext.size() + AES_BLOCK_SIZE);

    EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, aes_key, aes_iv);
    EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size());
    plaintext_len = len;
    EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len);
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);
    plaintext.resize(plaintext_len);
    return plaintext_len;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;

    std::ifstream infile(argv[1], std::ios::binary);
    std::vector<unsigned char> ciphertext((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    std::vector<unsigned char> plaintext;

    decrypt(ciphertext, plaintext);
    std::string decrypted((char*)plaintext.data(), plaintext.size());

    size_t pos = decrypted.find("::");
    if (pos != std::string::npos) {
        std::string filename = decrypted.substr(0, pos);
        std::string content = decrypted.substr(pos + 2);

        // Vulnerability: Path traversal. No sanitization of 'filename'
        std::string filepath = "/home/user/uploads/" + filename;
        std::ofstream outfile(filepath, std::ios::binary);
        outfile << content;
        outfile.close();
    }
    return 0;
}
EOF

    g++ /tmp/upload_agent.cpp -lcrypto -o /home/user/upload_agent
    rm /tmp/upload_agent.cpp

    chmod -R 777 /home/user