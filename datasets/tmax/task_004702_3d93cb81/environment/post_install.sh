apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app/bin
    touch /app/incident_evidence.mp4
    touch /home/user/core.dump
    touch /home/user/extract_metadata.py
    touch /home/user/process.sh
    touch /app/bin/extract_metadata_oracle
    chmod +x /app/bin/extract_metadata_oracle

    chmod -R 777 /home/user