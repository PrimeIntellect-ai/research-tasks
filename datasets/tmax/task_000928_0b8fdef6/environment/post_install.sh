apt-get update && apt-get install -y python3 python3-pip g++ netcat-openbsd nodejs curl
    pip3 install pytest

    mkdir -p /home/user/bin
    mkdir -p /home/user/cron
    mkdir -p /home/user/services/backup_data
    mkdir -p /home/user/backups
    mkdir -p /home/user/workspace

    cat << 'EOF' > /home/user/workspace/ref.cpp
#include <iostream>
int main(int argc, char** argv) {
    return 0;
}
EOF
    g++ /home/user/workspace/ref.cpp -o /home/user/bin/manifest_checker_ref
    rm /home/user/workspace/ref.cpp

    cat << 'EOF' > /home/user/cron/backup_job.sh
#!/bin/bash
# Buggy script
echo "Running backup..." > /tmp/manifest.log
EOF
    chmod +x /home/user/cron/backup_job.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user