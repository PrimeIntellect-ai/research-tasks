apt-get update && apt-get install -y python3 python3-pip git gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/edge_case_trace.log
Connection established.
Source: 192.168.1.50
Dest IP: 10.0.0.5
Intermediate state traced. Packet dropped.
Src IP:  172.16.254.1
Target   IP: 8.8.8.8
Invalid packet: 256.0.0.1
Malformed trace: SourceIP:1.1.1.1
EOF

    mkdir -p /home/user/net-parser
    cd /home/user/net-parser

    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    cat << 'EOF' > parse_trace.sh
#!/bin/bash
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$1" | awk -F. '$1<=255 && $2<=255 && $3<=255 && $4<=255' | sort -u
EOF
    chmod +x parse_trace.sh

    git add parse_trace.sh
    git commit -m "Initial commit: robust IP extraction"
    git tag v1.0

    for i in {1..125}; do
        echo "# comment $i" >> parse_trace.sh
        git commit -am "Update script: minor change $i"
    done

    cat << 'EOF' > parse_trace.sh
#!/bin/bash
# Optimized parsing
awk '{for(i=1;i<=NF;i++) if($i ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) print $i}' "$1" | awk -F. '$1<=255 && $2<=255 && $3<=255 && $4<=255' | sort -u
EOF
    chmod +x parse_trace.sh
    git commit -am "Optimize IP extraction using awk"
    BAD_COMMIT=$(git rev-parse HEAD)

    for i in {127..200}; do
        echo "# extra comment $i" >> parse_trace.sh
        git commit -am "Update script: minor change $i"
    done

    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chmod -R 777 /home/user