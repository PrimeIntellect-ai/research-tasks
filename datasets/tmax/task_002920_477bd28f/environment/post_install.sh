apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        wget \
        curl \
        libcurl4

    pip3 install pytest pymongo

    # Create dummy video
    mkdir -p /app
    ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=30 -c:v libx264 -g 15 /app/telemetry.mp4

    # Install MongoDB from binary tarball
    wget -q https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-6.0.16.tgz
    tar -zxvf mongodb-linux-x86_64-ubuntu2204-6.0.16.tgz
    cp mongodb-linux-x86_64-ubuntu2204-6.0.16/bin/* /usr/local/bin/
    rm -rf mongodb-linux-x86_64-ubuntu2204-6.0.16*

    mkdir -p /data/db
    chmod -R 777 /data/db

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user