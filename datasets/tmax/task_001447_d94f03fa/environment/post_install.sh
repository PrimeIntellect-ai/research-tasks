apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user

    # 1. Create the mock memory dump
    dd if=/dev/urandom of=/home/user/memory.dmp bs=1K count=10 2>/dev/null
    echo -n "AUTH_TOKEN=aB9xQp2L5k99V" >> /home/user/memory.dmp
    dd if=/dev/urandom bs=1K count=10 2>/dev/null >> /home/user/memory.dmp

    # 2. Create the buggy legacy script
    cat << 'EOF' > /home/user/legacy_processor.sh
#!/bin/bash

input=$1

if [ ! -f "$input" ]; then
    echo "File not found"
    exit 1
fi

while IFS=, read -r req_id user status message; do
    # Bug: if status is empty or non-numeric, this crashes bash because of set -e
    if [ $status -ge 400 ]; then
        echo "ERROR: $req_id - $message"
    else
        echo "OK: $req_id"
    fi
done < "$input"
EOF
    chmod +x /home/user/legacy_processor.sh

    # 3. Create the raw data with an edge case
    cat << 'EOF' > /home/user/raw_data.csv
101,alice,200,success
102,bob,404,not_found
103,charlie,,timeout
104,dave,500,server_error
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user