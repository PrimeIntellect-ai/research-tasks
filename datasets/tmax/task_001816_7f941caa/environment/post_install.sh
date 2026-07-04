apt-get update && apt-get install -y python3 python3-pip openssh-server openssl espeak
    pip3 install pytest

    mkdir -p /app

    # Generate the audio dictation
    espeak -w /app/assessment_dictation.wav "During the authentication flow test on the staging server, we noticed several legacy configurations. For SSH, we found aes128-cbc, 3des-cbc, and arcfour left enabled. For the web server TLS, both TLS version 1.0 and TLS version 1.1 are still accepting connections. Please verify these immediately."

    # Setup SSH server
    mkdir -p /run/sshd
    chmod 0755 /run/sshd
    ssh-keygen -A

    # Setup TLS server certificates
    openssl req -x509 -newkey rsa:2048 -keyout /app/key.pem -out /app/cert.pem -days 365 -nodes -subj "/CN=localhost"

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app