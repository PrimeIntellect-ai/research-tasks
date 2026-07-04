apt-get update && apt-get install -y python3 python3-pip gcc netcat
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/audit

    # Create dummy tar and sha256
    echo "dummy content" > /home/user/audit/server_config.tar.gz
    cd /home/user/audit
    sha256sum server_config.tar.gz > server_config.tar.gz.sha256

    # Create traffic log
    cat << 'EOF' > /home/user/audit/traffic.log
192.168.1.10 [10/Oct/2023:13:55:36] "GET /login?redirect=/home&token=9a HTTP/1.1" 200
10.0.0.5 [10/Oct/2023:13:56:01] "GET /login?redirect=http://malicious.com&token=ff HTTP/1.1" 200
172.16.0.42 [10/Oct/2023:13:57:11] "GET /login?redirect=https://evil.org&token=b3 HTTP/1.1" 200
203.0.113.8 [10/Oct/2023:13:58:22] "GET /login?redirect=http://phish.net&token=c1 HTTP/1.1" 200
EOF

    chmod -R 777 /home/user