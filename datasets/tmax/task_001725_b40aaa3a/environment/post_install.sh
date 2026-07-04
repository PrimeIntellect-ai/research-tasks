apt-get update && apt-get install -y python3 python3-pip ffmpeg openssh-server
    pip3 install pytest flask requests

    # Create dummy video file
    mkdir -p /app
    ffmpeg -f lavfi -i color=c=black:s=128x128:r=10 -t 1 /app/surveillance.mp4

    # Setup HTTP server directory
    mkdir -p /var/www
    echo -n "secret_token_99x" > /var/www/token

    # Setup SSH server and user
    mkdir -p /run/sshd
    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/.ssh
    ssh-keygen -t rsa -b 2048 -f /home/user/.ssh/id_rsa -N ""
    cat /home/user/.ssh/id_rsa.pub > /home/user/.ssh/authorized_keys

    # Flawed SSH config
    cat << 'EOF' > /home/user/.ssh/config
Host auth-service
    HostName localhost
    Port 2222
    User user
    PubkeyAuthentication no
EOF

    chmod 700 /home/user/.ssh
    chmod 600 /home/user/.ssh/*
    chown -R user:user /home/user/.ssh

    chmod -R 777 /home/user