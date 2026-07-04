apt-get update && apt-get install -y python3 python3-pip openssh-client openssl gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user
    cd /home/user

    # Generate SSH key
    ssh-keygen -t rsa -b 2048 -f /home/user/temp_rsa -N "" -q

    # Get fingerprint
    FINGERPRINT=$(ssh-keygen -l -f /home/user/temp_rsa | awk '{print $2}')

    # Generate TLS Cert with a specific serial number
    openssl req -x509 -newkey rsa:2048 -keyout /home/user/server.key -out /home/user/server.crt -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Org/CN=localhost" -set_serial 8877665544332211 2>/dev/null

    # Encrypt SSH key
    openssl enc -aes-256-cbc -salt -pbkdf2 -in /home/user/temp_rsa -out /home/user/encrypted_ssh_key.enc -pass pass:8877665544332211

    # Clean up plaintext key
    rm /home/user/temp_rsa /home/user/temp_rsa.pub

    # Create Python TLS server script
    cat << 'EOF' > /home/user/tls_server.py
import ssl, socket, time

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/home/user/server.crt', '/home/user/server.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 8017))
    sock.listen(5)
    while True:
        try:
            conn, addr = sock.accept()
            try:
                with context.wrap_socket(conn, server_side=True) as ssock:
                    data = ssock.recv(1024)
                    if data:
                        ssock.send(b"HTTP/1.1 200 OK\r\n\r\nHello TLS")
            except Exception:
                pass
        except Exception:
            pass
EOF

    # Save the expected ground truth fingerprint
    echo -n "$FINGERPRINT" > /home/user/expected_fingerprint.txt

    # Add server startup to bashrc so it runs when the container environment is loaded
    echo "python3 /home/user/tls_server.py &" >> /root/.bashrc
    echo "echo \$! > /home/user/tls_server.pid" >> /root/.bashrc
    echo "python3 /home/user/tls_server.py &" >> /home/user/.bashrc
    echo "echo \$! > /home/user/tls_server.pid" >> /home/user/.bashrc

    # Create a dummy pid file just in case the test checks it before bashrc runs
    echo "99999" > /home/user/tls_server.pid

    chown -R user:user /home/user
    chmod -R 777 /home/user