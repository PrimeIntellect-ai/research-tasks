apt-get update && apt-get install -y python3 python3-pip git espeak
    pip3 install pytest

    mkdir -p /home/user/audio_service
    cd /home/user/audio_service

    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"
    echo "CALIBRATION_CONSTANT = 0.9824" > config.py
    git add config.py
    git commit -m "Initial commit with calibration"
    echo "CALIBRATION_CONSTANT = 1.0" > config.py
    git add config.py
    git commit -m "Accidentally removed calibration constant"

    cat << 'EOF' > processor.py
import threading

_debug_history = []
lock_A = threading.Lock()
lock_B = threading.Lock()

def process(x, beta):
    y = [0] * len(x)
    for n in range(1, len(x)):
        y[n] = x[n] + 0.5 * y[n-1] / (beta - x[n])
    return y
EOF

    echo "encrypted dump" > crash.dmp.enc

    mkdir -p /app
    espeak -w /app/trigger_signal.wav "four eight one five one six"

    touch /app/oracle_processor
    chmod +x /app/oracle_processor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user