apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create directories
    mkdir -p /app/src

    # Create dummy input corrupted wav
    echo "RIFF....WAVEfmt ........data...." > /app/input_corrupted.wav

    # Create dummy broken setup script and source code
    echo "import os" > /app/src/setup.py
    echo "def process(): pass" > /app/src/main.py

    # Create dummy oracle processor
    echo '#!/usr/bin/env python3' > /app/oracle_processor
    echo 'print("oracle")' >> /app/oracle_processor
    chmod +x /app/oracle_processor

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user