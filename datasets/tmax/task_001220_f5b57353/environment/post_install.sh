apt-get update && apt-get install -y python3 python3-pip g++ curl tar netcat-openbsd
    pip3 install pytest aiosmtpd

    # Create directories and backup archive
    mkdir -p /app/backups
    cd /app/backups
    echo "dummy app" > app.bin
    echo '{"config": "dummy"}' > config.json
    tar -czf v1.0.tar.gz app.bin config.json
    rm app.bin config.json

    # Create SMTP server script
    cat << 'EOF' > /app/smtp_server.py
import asyncio
from aiosmtpd.controller import Controller

class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        with open('/home/user/mail.log', 'a') as f:
            f.write(f"MAIL FROM: {envelope.mail_from}\n")
            for rcpt in envelope.rcpt_tos:
                f.write(f"RCPT TO:<{rcpt}>\n")
            f.write(f"{envelope.content.decode('utf8', errors='replace')}\n")
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    controller = Controller(CustomHandler(), hostname='127.0.0.1', port=2525)
    controller.start()
    import time
    while True:
        time.sleep(1)
EOF

    # Setup user
    useradd -m -s /bin/bash user || true
    touch /home/user/mail.log
    chmod -R 777 /home/user