apt-get update && apt-get install -y python3 python3-pip golang ffmpeg openssh-server openssh-client curl jq
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Setup SSH directory and keys
    mkdir -p /home/user/.ssh
    ssh-keygen -t rsa -N "" -f /home/user/.ssh/id_rsa
    cp /home/user/.ssh/id_rsa.pub /home/user/.ssh/authorized_keys

    # Create SSH config with the misconfiguration
    cat << 'EOF' > /home/user/.ssh/config
Host local-monitor
    HostName 127.0.0.1
    User user
    IdentityFile /home/user/.ssh/wrong_key
    LocalForward 9090 127.0.0.1:8080
    IdentitiesOnly yes
EOF

    # Create deploy artifacts
    mkdir -p /home/user/deploy_artifacts
    head -c 1048576 /dev/urandom > /home/user/deploy_artifacts/dummy.bin
    echo "test" > /home/user/deploy_artifacts/test.txt

    # Create video fixture
    mkdir -p /app
    ffmpeg -f lavfi -i color=c=red:s=320x240:d=5 -c:v libx264 -y /app/dashboard.mp4

    # Ensure sshd can run
    mkdir -p /run/sshd

    # Final permissions (agent will need to fix SSH permissions as part of the task)
    chmod -R 777 /home/user