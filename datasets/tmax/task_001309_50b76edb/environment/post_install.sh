apt-get update && apt-get install -y python3 python3-pip tar coreutils
    pip3 install pytest

    mkdir -p /home/user/storage_dump/archives
    mkdir -p /home/user/storage_dump/logs
    mkdir -p /home/user/storage_dump/docs/nested

    # Create files for deduplication
    echo "Duplicate content A" > /home/user/storage_dump/docs/file1.txt
    echo "Duplicate content A" > /home/user/storage_dump/docs/nested/file2.txt
    echo "Duplicate content A" > /home/user/storage_dump/docs/nested/file3.txt

    echo "Unique content B" > /home/user/storage_dump/docs/file4.txt
    echo "Duplicate content C" > /home/user/storage_dump/file5.txt
    echo "Duplicate content C" > /home/user/storage_dump/logs/file6.txt

    # Create multi-part archive
    mkdir -p /tmp/backup_src
    echo "Secret Backup Data" > /tmp/backup_src/secret.txt
    tar -czf /tmp/backup.tar.gz -C /tmp backup_src
    split -b 100 /tmp/backup.tar.gz /home/user/storage_dump/archives/system_backup.tar.gz.
    rm -rf /tmp/backup_src /tmp/backup.tar.gz

    # Create log files with multi-line records
    cat << 'EOF' > /home/user/storage_dump/logs/app1.log
INFO: App started
[CRITICAL_START]
Error ID: 101
Module: Auth
Reason: Timeout
[CRITICAL_END]
DEBUG: retrying
EOF

    cat << 'EOF' > /home/user/storage_dump/logs/app2.log
WARN: low memory
[CRITICAL_START]
Error ID: 102
Module: DB
Reason: OOM
[CRITICAL_END]
INFO: shutting down
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user