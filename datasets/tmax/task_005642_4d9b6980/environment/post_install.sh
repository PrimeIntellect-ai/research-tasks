apt-get update && apt-get install -y python3 python3-pip sudo build-essential zlib1g-dev
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/user
    chmod 0440 /etc/sudoers.d/user

    mkdir -p /home/user/logs

    cat << 'EOF' > /home/user/logs/app_a.csv
1677632123,101,10,256
1677632124,102,11,512
EOF

    cat << 'EOF' > /home/user/logs/app_b.csv
1677632125,103,12,1024
1677632126,104,13,2048
EOF

    cat << 'EOF' > /home/user/logs/app_c.csv
1677632127,105,14,4096
1677632128,106,15,8192
EOF

    chmod -R 777 /home/user