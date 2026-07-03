apt-get update && apt-get install -y python3 python3-pip curl gnupg
    pip3 install pytest

    # Install MongoDB 6.0 and Go
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" > /etc/apt/sources.list.d/mongodb-org-6.0.list
    apt-get update
    apt-get install -y mongodb-org golang-go

    # Create MongoDB data and log directories
    mkdir -p /data/db /var/log/mongodb
    chmod -R 777 /data/db /var/log/mongodb

    # Create user and app directory
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/app

    # Initialize Go module and get mongo driver
    cd /home/user/app
    go mod init app
    go get go.mongodb.org/mongo-driver/mongo

    chmod -R 777 /home/user