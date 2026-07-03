apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/traffic.log
[10:00:01] 192.168.1.10 - user - 06400600
[10:01:23] 192.168.1.15 - test - 07561006
[10:05:44] 10.0.0.5 - guest - 144606111d
[10:12:05] 172.16.0.2 - backup - 115200091c43
EOF

    chmod -R 777 /home/user