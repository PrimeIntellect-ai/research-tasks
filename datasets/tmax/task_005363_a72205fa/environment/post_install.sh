apt-get update && apt-get install -y python3 python3-pip nginx redis-server golang-go curl
    pip3 install pytest redis requests

    # Create data directories
    mkdir -p /app/data/clean
    mkdir -p /app/data/evil

    # Configure Nginx to serve /app/data on port 8080 under /data/
    cat << 'EOF' > /etc/nginx/sites-available/default
server {
    listen 8080 default_server;
    listen [::]:8080 default_server;

    server_name _;

    location /data/ {
        alias /app/data/;
        autoindex on;
    }
}
EOF

    # Ensure permissions
    chmod -R 777 /app/data

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user