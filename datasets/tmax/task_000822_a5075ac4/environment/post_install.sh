apt-get update && apt-get install -y python3 python3-pip ffmpeg golang-go
    pip3 install pytest pandas numpy

    mkdir -p /app
    # Generate a short synthetic video for testing
    ffmpeg -y -f lavfi -i testsrc=duration=5:size=320x240:rate=30 -c:v libx264 -preset ultrafast /app/data_feed.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user