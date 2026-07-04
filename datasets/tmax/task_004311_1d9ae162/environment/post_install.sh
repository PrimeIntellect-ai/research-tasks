apt-get update && apt-get install -y python3 python3-pip gcc libssl-dev openssl
    pip3 install pytest

    mkdir -p /app/corpora/evil /app/corpora/clean

    # Generate cert_validator
    cat << 'EOF' > /tmp/cert_validator.c
#include <stdio.h>
#include <string.h>
#include <openssl/md5.h>
#include <openssl/x509.h>
#include <openssl/pem.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    X509 *cert = PEM_read_X509(f, NULL, NULL, NULL);
    fclose(f);
    if (!cert) return 1;

    X509_NAME *subj = X509_get_subject_name(cert);
    int loc = X509_NAME_get_index_by_NID(subj, NID_organizationalUnitName, -1);
    if (loc == -1) return 1;
    X509_NAME_ENTRY *entry = X509_NAME_get_entry(subj, loc);
    ASN1_STRING *data = X509_NAME_ENTRY_get_data(entry);
    const char *ou = (const char *)ASN1_STRING_get0_data(data);

    unsigned char digest[MD5_DIGEST_LENGTH];
    MD5((unsigned char*)ou, strlen(ou), digest);
    char mdString[33];
    for(int i = 0; i < 16; i++)
        sprintf(&mdString[i*2], "%02x", (unsigned int)digest[i]);

    if(strcmp(mdString, "81216d251bc8cc3eb2a2ddc1e7a0fbc5") == 0) {
        return 0; // backdoor
    }
    return 1;
}
EOF
    gcc -O2 /tmp/cert_validator.c -o /app/cert_validator -lssl -lcrypto
    strip /app/cert_validator
    rm /tmp/cert_validator.c

    # Generate corpora
    for i in $(seq 1 50); do
        openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
            -subj "/C=US/ST=State/L=City/O=Organization/OU=dragon/CN=evil${i}.com" \
            -keyout /dev/null -out /app/corpora/evil/cert_${i}.pem 2>/dev/null
    done

    for i in $(seq 1 50); do
        openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
            -subj "/C=US/ST=State/L=City/O=Organization/OU=clean${i}/CN=clean${i}.com" \
            -keyout /dev/null -out /app/corpora/clean/cert_${i}.pem 2>/dev/null
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user