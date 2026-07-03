apt-get update && apt-get install -y python3 python3-pip openssl gawk coreutils
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/certs
cd /home/user/certs

# Generate CA
openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout ca.key -out ca.crt -subj "/CN=Internal CA"

# Generate Server Key and CSR
openssl req -newkey rsa:2048 -nodes -keyout temp_server.key -out server.csr -subj "/CN=server.local"

# Sign Server Cert
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Encrypt the server key with a password ("supersecret123")
openssl rsa -in temp_server.key -out encrypted_server.key -aes256 -passout pass:supersecret123

# Base64 encode the encrypted key
base64 encrypted_server.key > /home/user/certs/encrypted_key.b64

# Clean up temporary/unencrypted files
rm ca.key temp_server.key server.csr encrypted_server.key

# Create wordlist
cat << 'EOF' > /home/user/wordlist.txt
password
admin123
letmein99
supersecret123
qwerty
winter2023
EOF

chown -R user:user /home/user/certs /home/user/wordlist.txt
chmod -R 777 /home/user