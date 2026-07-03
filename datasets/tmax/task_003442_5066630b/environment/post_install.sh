apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install dependencies for Rust, audio processing, and TTS
    apt-get install -y cargo espeak-ng ffmpeg curl build-essential

    # Create the /app directory
    mkdir -p /app

    # Generate the audio file with the hidden parameters
    espeak-ng -w /app/memo.wav "Hi, please use a rolling window size of exactly four items. Also, when you tokenize the notes, make sure to filter out the word redacted. Thanks."

    # Create the user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user