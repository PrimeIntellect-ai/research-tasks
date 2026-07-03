apt-get update && apt-get install -y python3 python3-pip espeak openssl
    pip3 install pytest cryptography

    mkdir -p /app/certs
    mkdir -p /app/code/cert1
    mkdir -p /app/code/cert2
    mkdir -p /app/code/cert3

    # Generate audio
    espeak -w /app/compliance_audio.wav "Server Alpha uses the certificate ending in E 4 F 1. The codebase is vulnerable to CWE 79. Server Beta uses the certificate ending in 9 B A 2. The codebase is vulnerable to CWE 89. Server Gamma uses the certificate ending in 3 3 C D. The codebase is vulnerable to CWE 22."

    # Create code files
    cat << 'EOF' > /app/code/cert1/index.php
<?php
// CWE-79: Cross-Site Scripting
$user_input = $_GET['input'];
echo "<div>" . $user_input . "</div>";
?>
EOF

    cat << 'EOF' > /app/code/cert2/query.py
import sqlite3
# CWE-89: SQL Injection
def get_user(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)
    return cursor.fetchall()
EOF

    cat << 'EOF' > /app/code/cert3/fetch.c
#include <stdio.h>
#include <stdlib.h>
// CWE-22: Path Traversal
int main(int argc, char *argv[]) {
    if (argc > 1) {
        char filepath[256];
        sprintf(filepath, "/var/www/html/%s", argv[1]);
        FILE *f = fopen(filepath, "r");
        if (f) {
            // Read and print file
            fclose(f);
        }
    }
    return 0;
}
EOF

    # Generate certificates and truth.json using python
    cat << 'EOF' > /app/generate_certs.py
import os
import datetime
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from cryptography import x509

def generate_ca():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"RootCA")])
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(private_key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650)).add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True).sign(private_key, hashes.SHA256())
    with open("/app/certs/rootCA.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    return private_key, cert

def generate_cert(name, target_ending, is_valid, ca_key, ca_cert):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, name)])

    issuer_name = ca_cert.subject if is_valid else subject
    signing_key = ca_key if is_valid else private_key

    while True:
        serial = x509.random_serial_number()
        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer_name).public_key(private_key.public_key()).serial_number(serial).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).sign(signing_key, hashes.SHA256())

        der = cert.public_bytes(serialization.Encoding.DER)
        fp = hashes.Hash(hashes.SHA256())
        fp.update(der)
        digest = fp.finalize().hex()

        if digest.endswith(target_ending):
            with open(f"/app/certs/{name}.crt", "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            return digest

ca_key, ca_cert = generate_ca()
fp1 = generate_cert('cert1', 'e4f1', True, ca_key, ca_cert)
fp2 = generate_cert('cert2', '9ba2', False, ca_key, ca_cert)
fp3 = generate_cert('cert3', '33cd', True, ca_key, ca_cert)

truth = {
  "alpha": {
    "certificate_file": "cert1.crt",
    "full_sha256_fingerprint": fp1,
    "chain_valid": True,
    "cwe_id": 79
  },
  "beta": {
    "certificate_file": "cert2.crt",
    "full_sha256_fingerprint": fp2,
    "chain_valid": False,
    "cwe_id": 89
  },
  "gamma": {
    "certificate_file": "cert3.crt",
    "full_sha256_fingerprint": fp3,
    "chain_valid": True,
    "cwe_id": 22
  }
}
with open('/app/truth.json', 'w') as f:
    json.dump(truth, f)
EOF

    python3 /app/generate_certs.py
    rm /app/generate_certs.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user