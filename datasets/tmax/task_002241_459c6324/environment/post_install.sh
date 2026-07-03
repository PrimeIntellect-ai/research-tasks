apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest
    apt-get install -y qemu-system-x86 cron netcat-openbsd procps

    useradd -m -s /bin/bash user || true

    mkdir -p /var/spool/cron/crontabs
    touch /var/spool/cron/crontabs/user
    chown user:crontab /var/spool/cron/crontabs/user
    chmod 600 /var/spool/cron/crontabs/user

    chmod -R 777 /home/user