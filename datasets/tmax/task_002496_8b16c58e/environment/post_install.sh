apt-get update && apt-get install -y python3 python3-pip golang ffmpeg tesseract-ocr
    pip3 install pytest

    mkdir -p /app
    touch /app/config_dashboard.mp4

    # Create dummy oracle parser for initial state tests
    touch /app/oracle_parser
    chmod +x /app/oracle_parser

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user