apt-get update && apt-get install -y python3 python3-pip ffmpeg openssl john
    pip3 install pytest

    mkdir -p /app

    # Create wordlist
    cat << 'EOF' > /app/wordlist.txt
password123
admin123
devsecops
enforce2024
secure2023
policy_admin
EOF

    # Create dummy policy and encrypt it
    cat << 'EOF' > /app/policy_raw.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
EOF
    openssl aes-256-cbc -salt -pbkdf2 -in /app/policy_raw.txt -out /app/policy.enc -pass pass:enforce2024
    rm /app/policy_raw.txt

    # Create subtitle file and generate MP4 with it
    cat << 'EOF' > /tmp/sub.srt
1
00:00:00,000 --> 00:00:05,000
Admin Hash: 8b0f496359e93bc4c9bb4b6b6ecaf4e7
EOF
    ffmpeg -f lavfi -i color=c=black:s=320x240:d=5 -i /tmp/sub.srt -c:v libx264 -c:s mov_text -map 0:v -map 1:s /app/audit_recording.mp4
    rm /tmp/sub.srt

    # Create oracle checker
    cat << 'EOF' > /app/oracle_checker
#!/bin/bash
DIR="$1"
policy="/home/user/policy.txt"
if [ ! -f "$policy" ]; then
    touch "$policy"
fi

find "$DIR" -maxdepth 1 -type f -print0 | sort -z | while IFS= read -r -d '' file; do
    hash=$(sha256sum "$file" | awk '{print $1}')
    filename=$(basename "$file")
    if grep -q "^$hash\$" "$policy"; then
        echo "[OK] $filename"
    else
        echo "[FAIL] $filename"
    fi
done
EOF
    chmod +x /app/oracle_checker

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user