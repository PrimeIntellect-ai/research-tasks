apt-get update && apt-get install -y python3 python3-pip coreutils bash
    pip3 install pytest

    mkdir -p /home/user

    # Create the fake ELF binary by copying an existing binary and appending the secret
    cp /bin/true /home/user/auth_handler
    chmod +x /home/user/auth_handler
    echo -n "PWD_c3VwZXJfc2VjcmV0X2FkbWluXzk5" >> /home/user/auth_handler

    # Create the CGI login script
    cat << 'EOF' > /home/user/login.cgi
#!/bin/bash

if [ "$1" == "super_secret_admin_99" ]; then
    echo -e "HTTP/1.1 302 Found\r"
    echo -e "Set-Cookie: session_id=abc123xyz890; Path=/; HttpOnly\r"
    echo -e "Location: http://malicious-site.local/redirect_target\r"
    echo -e "\r"
    echo -e "Authentication successful. Redirecting..."
else
    echo -e "HTTP/1.1 401 Unauthorized\r"
    echo -e "Content-Type: text/plain\r"
    echo -e "\r"
    echo -e "Invalid credentials."
fi
EOF
    chmod +x /home/user/login.cgi

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user