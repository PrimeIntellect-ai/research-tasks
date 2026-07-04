apt-get update && apt-get install -y python3 python3-pip openssl coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/certs /home/user/secrets /home/user/rotation

    # 1. Generate Certificates
    cd /home/user/certs
    # Root CA
    openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout rootCA.key -out rootCA.pem -subj "/CN=RootCA"
    # Intermediate CA
    openssl req -newkey rsa:2048 -nodes -keyout intermediate.key -out intermediate.csr -subj "/CN=IntermediateCA"
    openssl x509 -req -in intermediate.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out intermediate.pem -days 365
    # Service Cert
    openssl req -newkey rsa:2048 -nodes -keyout db_service.key -out db_service.csr -subj "/CN=DBService"
    openssl x509 -req -in db_service.csr -CA intermediate.pem -CAkey intermediate.key -CAcreateserial -out db_service.pem -days 365

    # 2. Setup legacy secret
    cd /home/user/secrets
    echo -n "SuperSecretDB99" | openssl enc -aes-256-cbc -pbkdf2 -pass pass:admin123 -out legacy_secret.enc

    # 3. Setup deploy script
    cat << 'EOF' > /home/user/deploy.sh
#!/bin/bash
if [ -n "$DEPLOY_HASH" ] && [ -z "$USER" ] && [ -z "$HOME" ]; then
    echo "Deployment triggered with hash: $DEPLOY_HASH" > /home/user/rotation/deploy.log
else
    echo "Error: Environment not properly isolated or DEPLOY_HASH missing." > /home/user/rotation/deploy.log
fi
EOF
    chmod +x /home/user/deploy.sh

    chown -R user:user /home/user/certs /home/user/secrets /home/user/rotation /home/user/deploy.sh
    chmod -R 777 /home/user