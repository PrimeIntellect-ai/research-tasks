apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest numpy flask fastapi uvicorn requests scipy

    mkdir -p /app
    touch /app/test_audio.wav
    chmod 777 /app/test_audio.wav

    mkdir -p /home/user/audio-service
    cd /home/user/audio-service
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    for i in $(seq 1 200); do
        echo "Commit $i" > file.txt
        git add file.txt
        git commit -m "Commit $i"
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app