apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/reference_profile.txt
Bin 0: 2164
Bin 1: 104
Bin 2: 60
Bin 3: 40
Bin 4: 36
Bin 5: 32
Bin 6: 28
Bin 7: 24
Bin 8: 12
Bin 9: 0
EOF

    chmod -R 777 /home/user