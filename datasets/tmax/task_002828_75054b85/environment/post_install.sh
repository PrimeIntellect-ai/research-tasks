apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/incremental_manifest.txt
data/user_uploads/image.png
../etc/passwd
data/../../etc/shadow
/var/log/syslog
data/config.json
scripts/..
normal_file.txt
sneaky..file.txt
..
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user