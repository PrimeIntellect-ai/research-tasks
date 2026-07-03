apt-get update && apt-get install -y python3 python3-pip ffmpeg cargo
    pip3 install pytest

    mkdir -p /app
    # Create a dummy video with base64 encoded title metadata
    ffmpeg -f lavfi -i color=c=black:s=16x16:d=1 -metadata title="ZHVtbXk=" /app/security_feed.mp4

    touch /app/oracle_processor
    chmod +x /app/oracle_processor

    mkdir -p /home/user/secure_router/src
    mkdir -p /home/user/secure_router/asm

    touch /home/user/secure_router/Cargo.toml
    touch /home/user/secure_router/src/main.rs
    touch /home/user/secure_router/src/parser.rs
    touch /home/user/secure_router/src/validator.rs
    touch /home/user/secure_router/asm/validator_x64.asm

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user