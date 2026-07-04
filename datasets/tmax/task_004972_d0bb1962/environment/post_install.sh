apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user/proc_dump/1024
    mkdir -p /home/user/proc_dump/2048
    mkdir -p /home/user/proc_dump/3096

    # Create mock cmdline files (null-byte separated)
    printf "init\0" > /home/user/proc_dump/1024/cmdline
    printf "/bin/bash\0/opt/backup.sh\0--user\0admin\0--pass-hash\0c21f969b5f03d33d43e04f8f136e7682\0" > /home/user/proc_dump/2048/cmdline
    printf "nginx\0-g\0daemon off;\0" > /home/user/proc_dump/3096/cmdline

    # Create wordlist
    cat << 'EOF' > /home/user/wordlist.txt
apple
banana
password
admin123
s3cr3t
hunter2
qwerty
letmein
EOF

    # Create the secret document
    echo "FLAG{b4sh_ev4s10n_m4st3r}" > /home/user/secret_document.txt

    # Create the runner script
    cat << 'EOF' > /home/user/runner.sh
#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <password> <payload>"
    exit 1
fi

HASH=$(echo -n "$1" | md5sum | awk '{print $1}')
if [ "$HASH" != "c21f969b5f03d33d43e04f8f136e7682" ]; then
    echo "Access Denied: Incorrect Password"
    exit 1
fi

PAYLOAD="$2"

# Security Policy Filter
if echo "$PAYLOAD" | grep -qE 'cat|head|tail|less|more|awk|sed|grep|base64|xxd|secret|document|flag|\\|'\''|"'; then
    echo "Security Policy Violation: Payload contains restricted characters or commands."
    exit 1
fi

echo "Executing payload..."
eval "$PAYLOAD"
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user