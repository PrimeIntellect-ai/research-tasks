apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        gcc \
        ffmpeg \
        flite \
        pocketsphinx \
        pocketsphinx-en-us \
        python3-pocketsphinx

    pip3 install pytest SpeechRecognition

    # Create the required audio file using flite
    mkdir -p /app
    flite -t "Incremental backups provide differential payload structures." -o /app/dictation.wav

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user