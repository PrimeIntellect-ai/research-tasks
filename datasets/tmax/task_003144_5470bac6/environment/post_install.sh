apt-get update && apt-get install -y python3 python3-pip festival
    pip3 install pytest

    mkdir -p /app
    echo "albatross" | text2wave -o /app/voicemail.wav

    cat << 'EOF' > /app/oracle_router
#!/usr/bin/env python3
import sys

def run_oracle(hex_str):
    s = "albatross"
    try:
        bytes_data = bytes.fromhex(hex_str)
    except ValueError:
        return s

    i = 0
    while i < len(bytes_data):
        op = bytes_data[i]
        if op == 0x00:
            break
        elif op == 0x01:
            s = s.upper()
        elif op == 0x02:
            s = s[::-1]
        elif op == 0x03:
            if i + 1 < len(bytes_data):
                n = bytes_data[i+1]
                s = s[n:]
                i += 1
        elif op == 0x04:
            if i + 1 < len(bytes_data):
                char_code = bytes_data[i+1]
                s += chr(char_code)
                i += 1
        elif op == 0x05:
            s = s.lower()
        i += 1
    return s

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(run_oracle(sys.argv[1]))
EOF

    chmod +x /app/oracle_router

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user