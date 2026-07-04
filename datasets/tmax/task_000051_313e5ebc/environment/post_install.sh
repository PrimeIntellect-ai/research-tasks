apt-get update && apt-get install -y python3 python3-pip espeak-ng
    pip3 install pytest

    # Create directories
    mkdir -p /app
    mkdir -p /home/user/service
    mkdir -p /home/user/logs

    # Generate the audio file
    espeak-ng -w /app/incident_log.wav "I managed to breach the server. I targeted the service running on port 8443. The old master secret I extracted is PURPLE_ELEPHANT_42. I bypassed the auth using the alg none JWT vulnerability."

    # Create log files with the secret
    echo "Failed login... secret used: PURPLE_ELEPHANT_42" > /home/user/logs/auth.log
    echo "Session started. key=PURPLE_ELEPHANT_42" > /home/user/logs/app.log

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app