apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        zbar-tools \
        openssl \
        qrencode

    pip3 install pytest

    mkdir -p /app

    # Generate dummy videos for the agent to use
    ffmpeg -f lavfi -i color=c=black:s=640x480:d=1 -c:v libx264 /app/admin_session.mp4
    ffmpeg -f lavfi -i color=c=black:s=640x480:d=1 -c:v libx264 /app/test_session.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app