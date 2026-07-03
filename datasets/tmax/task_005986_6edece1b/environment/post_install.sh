apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user

    # Create the application access log
    cat << 'EOF' > /home/user/app_access.log
[INFO] Service started on port 9000
[WARN] Rate limit exceeded for IP 192.168.1.50
[INFO] User guest logged in successfully
[ERROR] User admin failed authentication. Leaked hash: 71b7b41b80c2f35e95ba1143ec682e05
[INFO] Connection closed from 10.0.0.2
EOF

    # Create the wordlist
    cat << 'EOF' > /home/user/rockyou_subset.txt
password123
admin
qwerty
secret99
letmein
dragon
football
EOF

    # Create the vulnerable server script
    cat << 'EOF' > /home/user/server.py
import socket
import sys

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 9000))
    s.listen(1)
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(1024).decode('utf-8').strip()
            if data == "secret99":
                conn.sendall(b"FLAG{pwn3d_th3_c0py_p4st3_s3rv1c3}\n")
            else:
                conn.sendall(b"ACCESS DENIED\n")
            conn.close()
        except KeyboardInterrupt:
            break
    s.close()

if __name__ == "__main__":
    start_server()
EOF

    chmod 644 /home/user/app_access.log /home/user/rockyou_subset.txt
    chmod 755 /home/user/server.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user