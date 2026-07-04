apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/vulnerable_backup.sh
#!/bin/bash
INPUT_FILE=$1
OUTPUT_FILE=$2
PASSWORD=$3

if [ -z "$PASSWORD" ]; then
    echo "Usage: $0 <input> <output> <password>"
    exit 1
fi

# VULNERABILITY: Password passed directly via CLI argument
openssl enc -aes-256-cbc -pbkdf2 -in "$INPUT_FILE" -out "$OUTPUT_FILE" -pass pass:"$PASSWORD"
EOF
    chmod +x /home/user/vulnerable_backup.sh

    echo "FLAG{proc_cmdline_leaks_are_dangerous}" > /home/user/dummy_secret_internal.txt
    openssl enc -aes-256-cbc -pbkdf2 -in /home/user/dummy_secret_internal.txt -out /home/user/secret_data.enc -pass pass:"SuperSecretBackupP@ssw0rd2024"
    rm /home/user/dummy_secret_internal.txt

    cat << 'EOF' > /home/user/start_simulation.sh
#!/bin/bash
echo "Dummy data" > /tmp/dummy_input.txt
while true; do
    /home/user/vulnerable_backup.sh /tmp/dummy_input.txt /tmp/dummy_output.enc "SuperSecretBackupP@ssw0rd2024" >/dev/null 2>&1
    sleep 2
done
EOF
    chmod +x /home/user/start_simulation.sh

    chmod -R 777 /home/user