apt-get update && apt-get install -y python3 python3-pip procps
    pip3 install pytest

    mkdir -p /home/user

    # 1. Setup the hidden daemon script
    cat << 'EOF' > /home/user/.hidden_daemon.sh
#!/bin/bash
# Create secret file
echo "SECRET_KEY_99824_XOR_OBFUSCATION" > /tmp/.secret_key_tmp
# Open file descriptor 5 for reading
exec 5< /tmp/.secret_key_tmp
# Delete the file from filesystem
rm -f /tmp/.secret_key_tmp

# Loop forever to keep process and FD alive
while true; do
    sleep 60
done
EOF

    chmod +x /home/user/.hidden_daemon.sh

    # 2. Setup the buggy analyzer script
    cat << 'EOF' > /home/user/analyzer.sh
#!/bin/bash

if [ -z "$1" ] || [ ! -f "$1" ]; then
    echo "Usage: ./analyzer.sh <input_file>"
    exit 1
fi

sum=0
while IFS= read -r -n1 char; do
    # Skip empty characters
    if [[ -z "$char" ]]; then continue; fi

    # Get ASCII value
    val=$(printf "%d" "'$char")

    # BUG: divisor can be 0 if val is a multiple of 10
    divisor=$(( val % 10 ))

    # Calculate checksum
    sum=$(( (sum + val) / divisor ))
done < "$1"

echo "Final checksum: $sum"
EOF

    chmod +x /home/user/analyzer.sh

    # Create the user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user