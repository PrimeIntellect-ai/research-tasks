apt-get update && apt-get install -y python3 python3-pip git cron
    pip3 install pytest

    mkdir -p /home/user
    printf "root\nadmin\nguest\nsuperuser\n" > /home/user/banned_users.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user