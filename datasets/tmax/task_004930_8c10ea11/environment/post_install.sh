apt-get update && apt-get install -y python3 python3-pip openssl gawk coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/loot.txt
Target System Compromised.
Admin IP: 192.168.1.100
Backup Server: 10.0.0.52
User data found:
Alice - 123-45-6789 - Admin
Bob - 987-65-4321 - User
Network subnet: 172.16.0.0
EOF
    chmod 644 /home/user/loot.txt

    chmod -R 777 /home/user