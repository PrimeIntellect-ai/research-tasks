apt-get update && apt-get install -y python3 python3-pip build-essential curl
    pip3 install pytest

    mkdir -p /app
    cd /app
    pip3 download --no-binary :all: --no-deps Brotli==1.1.0
    tar -xzf Brotli-1.1.0.tar.gz
    mv Brotli-1.1.0 brotli-1.1.0
    rm Brotli-1.1.0.tar.gz

    # Introduce the deliberate typo in setup.py
    sed -i 's/extra_compile_args/extr_compile_args/g' /app/brotli-1.1.0/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user