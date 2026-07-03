apt-get update && apt-get install -y python3 python3-pip openssl gcc libc6-dev
    pip3 install pytest

    mkdir -p /home/user/certs
    cd /home/user/certs

    # Generate Root CA
    openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout root_ca.key -out root_ca.pem -subj "/CN=RootCA"
    # Generate Sub CA
    openssl req -newkey rsa:2048 -nodes -keyout sub_ca.key -out sub_ca.csr -subj "/CN=SubCA"
    openssl x509 -req -in sub_ca.csr -CA root_ca.pem -CAkey root_ca.key -CAcreateserial -out sub_ca.pem -days 365
    # Generate Service Cert
    openssl req -newkey rsa:2048 -nodes -keyout service.key -out service.csr -subj "/CN=Service"
    openssl x509 -req -in service.csr -CA sub_ca.pem -CAkey sub_ca.key -CAcreateserial -out service.pem -days 365

    cd /home/user
    # The new password
    NEW_PASS="CorrectHorseBatteryStaple2024!"

    # Create decryption key
    echo -n "t0pS3cr3tK3y" > /home/user/decryption_key.pass

    # Encrypt the password
    echo -n "$NEW_PASS" > /home/user/raw.txt
    openssl enc -aes-256-cbc -pbkdf2 -salt -in /home/user/raw.txt -out /home/user/new_cred.enc -pass file:/home/user/decryption_key.pass

    # Sign the encrypted file
    openssl dgst -sha256 -sign /home/user/certs/service.key -out /home/user/new_cred.sig /home/user/new_cred.enc

    rm /home/user/raw.txt

    # Create the legacy C program
    cat << 'EOF' > /home/user/legacy_auth.c
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return 1;
    }

    char *password = argv[1];

    // Simulate checking the credential
    if (strcmp(password, "CorrectHorseBatteryStaple2024!") == 0) {
        FILE *f = fopen("/home/user/rotation_success.log", "w");
        if (f) {
            fprintf(f, "Credential rotated successfully.\n");
            fclose(f);
            printf("Success.\n");
            return 0;
        }
    }

    printf("Authentication failed.\n");
    return 1;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user