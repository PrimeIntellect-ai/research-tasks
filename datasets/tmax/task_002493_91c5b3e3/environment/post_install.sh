apt-get update && apt-get install -y python3 python3-pip wget tar
    pip3 install pytest

    # Create /app and vendor dpkt-1.9.8
    mkdir -p /app
    cd /app
    pip3 download dpkt==1.9.8 --no-deps --no-binary :all:
    tar -xzf dpkt-1.9.8.tar.gz
    rm dpkt-1.9.8.tar.gz

    # Introduce the perturbation in dpkt/ssl.py
    sed -i "s/>H/>h/g" dpkt-1.9.8/dpkt/ssl.py

    # Create dummy oracle binary
    mkdir -p /opt/oracles
    touch /opt/oracles/traffic_analyzer_oracle.bin
    chmod +x /opt/oracles/traffic_analyzer_oracle.bin

    # Create user and home directory
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user