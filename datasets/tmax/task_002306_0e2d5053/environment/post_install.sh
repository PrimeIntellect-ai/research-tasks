apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest

    # Create the video directory and generate the reference video
    mkdir -p /app/video
    # Create a 15-second video at 30 fps (total 450 frames)
    ffmpeg -f lavfi -i color=c=black:s=640x480:r=30:d=15 -c:v libx264 -pix_fmt yuv420p /app/video/archive_footage.mp4

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user