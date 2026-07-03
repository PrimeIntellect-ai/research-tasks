apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest

    mkdir -p /app
    # Generate a 15-second test video
    ffmpeg -y -f lavfi -i testsrc=duration=15:size=640x480:rate=30 -pix_fmt yuv420p -c:v libx264 /app/surveillance.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user