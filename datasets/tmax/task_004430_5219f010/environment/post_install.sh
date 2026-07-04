apt-get update && apt-get install -y python3 python3-pip procps coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # 1. Create the dummy data processor script
    echo 'import time; time.sleep(10000)' > /home/user/data_processor.py
    chmod +x /home/user/data_processor.py

    # 2. Create the overly permissive certificate file
    echo "-----BEGIN PRIVATE KEY-----" > /home/user/private.pem
    echo "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQ..." >> /home/user/private.pem
    chmod 777 /home/user/private.pem

    # 3. Create the backup file and its valid SHA256 checksum
    echo "dummy backup data for verification" > /home/user/backup.zip
    sha256sum /home/user/backup.zip > /home/user/backup.zip.sha256

    chmod -R 777 /home/user