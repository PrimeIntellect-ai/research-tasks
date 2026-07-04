apt-get update && apt-get install -y python3 python3-pip curl espeak ffmpeg build-essential rustc cargo
    pip3 install pytest

    mkdir -p /app

    # Generate the audio file
    espeak -w /tmp/speech.wav "Calibration sequence alpha niner"
    ffmpeg -y -i /tmp/speech.wav -ar 16000 -ac 1 -c:a pcm_s16le /tmp/speech_16k.wav
    ffmpeg -y -f lavfi -i "sine=frequency=440:sample_rate=16000:duration=5" -f lavfi -i "sine=frequency=880:sample_rate=16000:duration=5" -filter_complex "[0:a][1:a]amix=inputs=2[sine]" -map "[sine]" -c:a pcm_s16le /tmp/sine.wav
    ffmpeg -y -i /tmp/sine.wav -i /tmp/speech_16k.wav -filter_complex "amix=inputs=2:duration=longest" -ar 16000 -ac 1 -c:a pcm_s16le /app/engine_test_run.wav

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app