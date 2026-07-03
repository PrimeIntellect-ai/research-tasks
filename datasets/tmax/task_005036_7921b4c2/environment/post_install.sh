apt-get update && apt-get install -y python3 python3-pip git tzdata gawk
    pip3 install pytest pandas numpy

    mkdir -p /app/bash-log-metrics/bin
    mkdir -p /home/user

    # Generate synthetic log file
    cat << 'EOF' > /home/user/prod_access.log
192.168.1.1 - - [2023-10-15T15:10:00Z] "GET /api/v1/users HTTP/1.1" 200 1024
192.168.1.2 - - [2023-10-15T15:20:00Z] "GET /api/v1/users HTTP/1.1" 500 512
192.168.1.3 - - [2023-10-15T16:05:00Z] "GET /api/v1/posts HTTP/1.1" 503 256
192.168.1.4 - - [2023-10-15T16:15:00Z] "GET /api/v1/posts HTTP/1.1" 500 256
192.168.1.5 - - [2023-10-15T16:25:00Z] "GET /api/v1/posts HTTP/1.1" 200 1024
192.168.1.6 - - [2023-10-15T17:00:00Z] "GET /api/v1/comments HTTP/1.1" 502 128
EOF

    # Create the aggregate script
    cat << 'EOF' > /app/bash-log-metrics/bin/aggregate.sh
#!/bin/bash
log_file=$1
echo "Hour,ErrorCount"
awk '{print $4, $9}' "$log_file" | tr -d '[]' | awk '$2 ~ /^5/ {print $1}' | while read timestamp; do
    bucket=$(TZ=UTC date -d "$timestamp" +'%Y-%m-%d %H:00')
    echo "$bucket"
done | sort | uniq -c | awk '{print $2 " " $3 "," $1}'
EOF
    chmod +x /app/bash-log-metrics/bin/aggregate.sh

    # Setup git repo
    cd /app/bash-log-metrics
    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"
    git init
    git add bin/aggregate.sh
    git commit -m "Initial commit"
    git tag v1.0.1

    # Generate ground truth
    /app/bash-log-metrics/bin/aggregate.sh /home/user/prod_access.log > /tmp/ground_truth.csv

    # Dummy commit 1
    echo "# dummy 1" >> bin/aggregate.sh
    git commit -am "chore: add dummy comment 1"

    # Dummy commit 2
    echo "# dummy 2" >> bin/aggregate.sh
    git commit -am "chore: add dummy comment 2"

    # Bad commit
    sed -i 's/TZ=UTC/TZ=America\/New_York/' bin/aggregate.sh
    git commit -am "feat: adjust timezone handling for local office"

    # Dummy commit 3
    echo "# dummy 3" >> bin/aggregate.sh
    git commit -am "chore: add dummy comment 3"

    # Dummy commit 4
    echo "# dummy 4" >> bin/aggregate.sh
    git commit -am "chore: add dummy comment 4"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app/bash-log-metrics