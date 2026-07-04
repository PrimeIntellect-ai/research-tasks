apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/source_data/app1/logs
    mkdir -p /home/user/source_data/app2/data
    mkdir -p /home/user/source_data/app3/logs/archive

    cat << 'EOF' > /home/user/source_data/app1/logs/server.log
[INFO] Server started
[CRITICAL] Database connection failed
[WARN] High memory usage
[CRITICAL] Out of memory error
EOF

    cat << 'EOF' > /home/user/source_data/app1/logs/notes.txt
[CRITICAL] Note: buy milk
EOF

    cat << 'EOF' > /home/user/source_data/app2/data/service.log
[INFO] Service running
[CRITICAL] Disk space critically low on /dev/sda1
[INFO] User logged in
[CRITICAL] Unauthorized access attempt detected from 192.168.1.50
[CRITICAL] Process crashed with segfault
EOF

    cat << 'EOF' > /home/user/source_data/app3/logs/archive/old.log
[CRITICAL] Thermal paste degraded, CPU temperature 99C
[WARN] Network latency high
[CRITICAL] Payment gateway timeout
[CRITICAL] Data corruption detected in sector 4
[CRITICAL] Fan failure
[CRITICAL] UPS battery depleted
[CRITICAL] Kernel panic - not syncing
[INFO] Shutdown complete
EOF

    cat << 'EOF' > /home/user/source_data/app3/logs/system.log
[CRITICAL] Active Directory sync failed
[CRITICAL] SSL certificate expired
[INFO] Backup successful
EOF

    chown -R user:user /home/user/source_data
    chmod -R 777 /home/user