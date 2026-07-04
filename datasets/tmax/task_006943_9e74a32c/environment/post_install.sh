apt-get update && apt-get install -y python3 python3-pip lsof systemd
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/app_data
    mkdir -p /home/user/mail_spool
    mkdir -p /home/user/.config/systemd/user

    chmod -R 777 /home/user