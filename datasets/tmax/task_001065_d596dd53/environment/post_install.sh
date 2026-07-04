apt-get update && apt-get install -y python3 python3-pip gawk coreutils
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/vulnerable_auth.sh
#!/bin/bash
# CGI Auth Gateway

USERNAME=${USER_ID:-""}
PASSWORD=${PASS_KEY:-""}
REDIRECT=${REDIR_URL:-"http://localhost/dashboard"}

# Hardcoded admin hash (MD5 of "s3cr3t_p4ss!")
ADMIN_HASH="74baee453b3dfdf7fb660bbf45ca462c"

CURRENT_HASH=$(echo -n "$PASSWORD" | md5sum | awk '{print $1}')

if [ "$USERNAME" == "admin" ] && [ "$CURRENT_HASH" == "$ADMIN_HASH" ]; then
    # URL Decode the redirect parameter naively
    DECODED_REDIRECT=$(echo -e "${REDIRECT//%/\\x}")

    echo "HTTP/1.1 302 Found"
    echo "Location: $DECODED_REDIRECT"
    echo "Content-Type: text/html"
    echo ""
    echo "<html><body>Redirecting...</body></html>"
else
    echo "HTTP/1.1 401 Unauthorized"
    echo "Content-Type: text/html"
    echo ""
    echo "<html><body>Invalid credentials</body></html>"
fi
EOF

    chmod +x /home/user/vulnerable_auth.sh

    cat << 'EOF' > /home/user/wordlist.txt
password123
admin
qwerty
s3cr3t_p4ss!
letmein
spring2024
welcome1
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user