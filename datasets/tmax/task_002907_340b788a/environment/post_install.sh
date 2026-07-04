apt-get update && apt-get install -y python3 python3-pip ffmpeg gzip
pip3 install pytest

mkdir -p /app
ffmpeg -f lavfi -i "sine=frequency=1000:duration=60" -ar 16000 -ac 1 /app/recording.wav -y

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user