apt-get update && apt-get install -y python3 python3-pip cron
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    printf "8000\n8001\n8002\n" > /home/user/ports.txt

    chmod -R 777 /home/user