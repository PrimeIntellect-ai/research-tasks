apt-get update && apt-get install -y python3 python3-pip espeak-ng
    pip3 install pytest

    # Create directories for corpora
    mkdir -p /app/corpora/clean
    mkdir -p /app/corpora/evil

    # Generate the audio file
    espeak-ng -w /app/voicemail.wav "The server error code is Delta Niner Two Five"

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user