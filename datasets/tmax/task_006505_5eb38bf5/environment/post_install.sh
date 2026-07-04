apt-get update && apt-get install -y python3 python3-pip curl cron procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/worker.sh
#!/bin/bash
while true; do
  curl -s http://localhost:8000/data > /dev/null
  echo "Pinged API" >> /var/log/worker.log
  sleep 5
done
EOF
    chmod +x /home/user/worker.sh

    # Ensure the mock API server is running when pytest is executed
    mv /usr/local/bin/pytest /usr/local/bin/pytest_orig
    cat << 'EOF' > /usr/local/bin/pytest
#!/bin/bash
if ! pgrep -f "http.server 8080" > /dev/null; then
    python3 -m http.server 8080 --bind 127.0.0.1 > /dev/null 2>&1 &
    sleep 1
fi
exec /usr/local/bin/pytest_orig "$@"
EOF
    chmod +x /usr/local/bin/pytest

    chmod -R 777 /home/user