apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/auth_handler.sh
#!/bin/bash
# Simple auth handler
USERNAME=$1
# Vulnerable to OS Command Injection (CWE-78)
eval "grep -i $USERNAME /etc/passwd"
EOF
    chmod +x /home/user/auth_handler.sh

    mkdir -p /home/user/certs
    cd /home/user/certs

    # Create CA
    openssl req -x509 -nodes -newkey rsa:2048 -keyout ca.key -out ca.crt -days 365 -subj "/CN=My Fake CA"

    # Create valid intermediate
    openssl req -new -nodes -newkey rsa:2048 -keyout intermediate.key -out intermediate.csr -subj "/CN=My Fake Intermediate"
    openssl x509 -req -in intermediate.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out intermediate.crt -days 365

    # Create INVALID server certificate (self-signed instead of signed by intermediate)
    openssl req -x509 -nodes -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -subj "/CN=My Fake Server"

    rm -f *.key *.csr *.srl

    cat << 'EOF' > /home/user/iptables_dump.txt
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 3306 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 8080 -s 127.0.0.1 -j ACCEPT
COMMIT
EOF

    chmod -R 777 /home/user