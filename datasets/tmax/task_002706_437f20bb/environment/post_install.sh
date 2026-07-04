apt-get update && apt-get install -y python3 python3-pip openssl libssl-dev gcc make
    pip3 install pytest

    mkdir -p /home/user/IR_case/ca /home/user/IR_case/server /home/user/IR_case/client

    # Generate CA
    openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout /home/user/IR_case/ca/ca.key -out /home/user/IR_case/ca/ca.crt -subj "/CN=AttackerCA"

    # Generate Server Cert
    openssl req -newkey rsa:2048 -nodes -keyout /home/user/IR_case/server/server.key -out /home/user/IR_case/server/server.csr -subj "/CN=server"
    openssl x509 -req -in /home/user/IR_case/server/server.csr -CA /home/user/IR_case/ca/ca.crt -CAkey /home/user/IR_case/ca/ca.key -CAcreateserial -out /home/user/IR_case/server/server.crt -days 365

    # Write the vulnerable server.c
    cat << 'EOF' > /home/user/IR_case/server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <openssl/evp.h>

#define PORT 8443

struct AuthData {
    char username[16];
    int is_admin;
};

void dump_intel() {
    FILE *f = fopen("/home/user/IR_case/intel.txt", "w");
    if (f) {
        fprintf(f, "FLAG{mTLS_and_mem_corrupt_master}\n");
        fclose(f);
        printf("Intel dropped.\n");
    }
}

int base64_decode(const char *encoded, unsigned char *decoded) {
    int len = strlen(encoded);
    int output_len = len * 3 / 4;
    EVP_DecodeBlock(decoded, (const unsigned char *)encoded, len);
    // Rough calculation, enough for this challenge
    return output_len;
}

void process_client(SSL *ssl) {
    char buf[1024] = {0};
    int bytes = SSL_read(ssl, buf, sizeof(buf) - 1);
    if (bytes > 0) {
        unsigned char decoded[1024] = {0};
        int dec_len = base64_decode(buf, decoded);

        // XOR decode
        for (int i = 0; i < dec_len; i++) {
            decoded[i] ^= 0x5A;
        }

        struct AuthData auth;
        auth.is_admin = 0;

        // VULNERABILITY: strcpy into fixed buffer
        strcpy(auth.username, (char*)decoded);

        if (auth.is_admin != 0) {
            dump_intel();
        } else {
            SSL_write(ssl, "Access Denied\n", 14);
        }
    }
}

int main() {
    SSL_CTX *ctx;
    SSL_library_init();
    OpenSSL_add_all_algorithms();
    SSL_load_error_strings();

    ctx = SSL_CTX_new(TLS_server_method());
    SSL_CTX_use_certificate_file(ctx, "/home/user/IR_case/server/server.crt", SSL_FILETYPE_PEM);
    SSL_CTX_use_PrivateKey_file(ctx, "/home/user/IR_case/server/server.key", SSL_FILETYPE_PEM);
    SSL_CTX_load_verify_locations(ctx, "/home/user/IR_case/ca/ca.crt", NULL);
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 1);

    while(1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);

        SSL *ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client_fd);

        if (SSL_accept(ssl) > 0) {
            process_client(ssl);
        }

        SSL_shutdown(ssl);
        SSL_free(ssl);
        close(client_fd);
    }
    close(server_fd);
    SSL_CTX_free(ctx);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/IR_case
    chmod -R 777 /home/user