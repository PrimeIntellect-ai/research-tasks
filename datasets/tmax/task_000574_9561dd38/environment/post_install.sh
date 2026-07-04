apt-get update && apt-get install -y python3 python3-pip nginx redis-server sqlite3 curl
    pip3 install pytest flask redis python-dotenv

    mkdir -p /home/user/app/nginx
    mkdir -p /home/user/app/backend
    mkdir -p /home/user/app/corpora/evil
    mkdir -p /home/user/app/corpora/clean

    # start.sh
    cat << 'EOF' > /home/user/app/start.sh
#!/bin/bash
nginx -c /home/user/app/nginx/nginx.conf &
redis-server &
cd /home/user/app/backend && python3 app.py &
wait
EOF
    chmod +x /home/user/app/start.sh

    # nginx.conf
    cat << 'EOF' > /home/user/app/nginx/nginx.conf
events {}
http {
    server {
        listen 8080;
        location / {
            proxy_pass http://127.0.0.1:5001;
        }
    }
}
EOF

    # backend/app.py
    cat << 'EOF' > /home/user/app/backend/app.py
import os
import threading
from flask import Flask, request
import redis

app = Flask(__name__)
r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"))

lock1 = threading.Lock()
lock2 = threading.Lock()

def task1():
    with lock1:
        with lock2:
            pass

def task2():
    with lock2:
        with lock1:
            pass

@app.route('/process', methods=['POST'])
def process():
    t1 = threading.Thread(target=task1)
    t2 = threading.Thread(target=task2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
EOF

    # backend/.env
    cat << 'EOF' > /home/user/app/backend/.env
REDIS_URL=redis://127.0.0.1:6380/0
EOF

    # exfiltrated.db and WAL
    touch /home/user/app/exfiltrated.db
    echo "SQLite format 3" > /home/user/app/exfiltrated.db
    echo "INSERT INTO payload_rules VALUES ('checksum', 'val = (header_len ^ 0x5A) + 12');" > /home/user/app/exfiltrated.db-wal

    # corpora files
    echo -ne "\x01\x02\x03\x04" > /home/user/app/corpora/evil/payload1.bin
    echo -ne "\x01\x02\x03\x04" > /home/user/app/corpora/clean/payload1.bin

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user