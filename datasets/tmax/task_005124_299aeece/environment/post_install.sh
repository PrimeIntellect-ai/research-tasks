apt-get update && apt-get install -y python3 python3-pip g++ netcat-openbsd
    pip3 install pytest

    mkdir -p /home/user/project_root
    mkdir -p /app/corpora/evil
    mkdir -p /app/corpora/clean
    mkdir -p /app/services

    cat << 'EOF' > /app/services/indexer.py
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9001))
s.listen(5)
while True:
    try:
        conn, addr = s.accept()
        with open('/app/services/raw_manifest.bin', 'rb') as f:
            conn.sendall(f.read())
        conn.close()
    except Exception:
        pass
EOF

    cat << 'EOF' > /app/services/storage.py
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9002))
s.listen(5)
while True:
    try:
        conn, addr = s.accept()
        data = b''
        while True:
            chunk = conn.recv(4096)
            if not chunk: break
            data += chunk
        with open('/app/services/received_manifest.bin', 'wb') as f:
            f.write(data)
        conn.close()
    except Exception:
        pass
EOF

    python3 -c "open('/app/services/raw_manifest.bin', 'wb').write(b'BKP_MNFS')"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app