apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /app/dataset/recordings/subfolder
    mkdir -p /app/dataset/metadata

    echo "dummy wav content" > /app/dataset/recordings/dummy1.wav
    touch /app/dataset/recordings/empty.wav
    touch /app/dataset/recordings/sample.wav

    ln -s /app/dataset/recordings /app/dataset/recordings/subfolder/loop_back
    ln -s /app/dataset /app/dataset/metadata/root_loop

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app