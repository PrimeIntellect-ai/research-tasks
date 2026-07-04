apt-get update && apt-get install -y python3 python3-pip util-linux coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/backups
    cd /home/user/backups

    cat << 'EOF' > server.log.txt
[INFO]
System initialized successfully.
PID: 1234
[/INFO]
[ERROR]
Database connection failed
Timeout: 30s
Module: Auth
[/ERROR]
[INFO]
Retrying connection...
[/INFO]
[ERROR]
Disk full
Path: /var/log
Module: Storage
[/ERROR]
[WARNING]
High memory usage
[/WARNING]
EOF

    iconv -f UTF-8 -t UTF-16LE server.log.txt > server.log
    tar -czf backup_3.tar.gz server.log

    size=$(stat -c%s backup_3.tar.gz)
    trunc_size=$((size - 50))
    dd if=backup_3.tar.gz of=backup_1.tar.gz bs=1 count=$trunc_size

    head -c 100 /dev/urandom > backup_2.tar.gz

    rm server.log.txt server.log

    chown -R user:user /home/user
    chmod -R 777 /home/user