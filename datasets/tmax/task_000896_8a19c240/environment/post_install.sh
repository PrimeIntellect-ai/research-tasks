apt-get update && apt-get install -y python3 python3-pip cargo rustc espeak
    pip3 install pytest

    mkdir -p /app
    espeak -w /app/telemetry_instructions.wav "Calculate the histogram using twenty bins spanning from zero to two point zero. Add one to all counts before taking the natural log."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user