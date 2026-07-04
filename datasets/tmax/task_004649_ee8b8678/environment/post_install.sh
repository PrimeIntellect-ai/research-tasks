apt-get update && apt-get install -y python3 python3-pip gawk coreutils
    pip3 install pytest

    # Create corpora directories
    mkdir -p /app/corpora/evil
    mkdir -p /app/corpora/clean

    # Create libsh-data vendored package
    mkdir -p /app/libsh-data-1.2.0/bin
    mkdir -p /app/libsh-data-1.2.0/lib

    cat << 'EOF' > /app/libsh-data-1.2.0/bin/sh-hash-row
#!/bin/bash
LIB_DIR="/opt/libsh-data/lib"
source "$LIB_DIR/normalize.sh"

if [ -z "$1" ]; then
    echo "Usage: $0 <sensor_id,value>"
    exit 1
fi

normalized=$(normalize_payload "$1")
echo -n "$normalized" | sha256sum | awk '{print $1}'
EOF
    chmod +x /app/libsh-data-1.2.0/bin/sh-hash-row

    cat << 'EOF' > /app/libsh-data-1.2.0/lib/normalize.sh
#!/bin/bash
normalize_payload() {
    local input="$1"
    # strip whitespace and lowercase
    echo "$input" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]'
}
EOF
    chmod +x /app/libsh-data-1.2.0/lib/normalize.sh

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user