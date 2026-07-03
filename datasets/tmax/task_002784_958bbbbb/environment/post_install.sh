apt-get update && apt-get install -y python3 python3-pip imagemagick fonts-liberation
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Create reference oracle
    cat << 'EOF' > /app/reference_oracle
#!/usr/bin/env python3
import sys

def main():
    data = sys.stdin.read()
    delimiter = "TERMINATE_TRANSACTION_99X"
    chunks = data.split(delimiter)
    reversed_chunks = [chunk[::-1] for chunk in chunks]
    sys.stdout.write(delimiter.join(reversed_chunks))

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/reference_oracle

    # Create buggy script
    cat << 'EOF' > /home/user/buggy_pipeline.sh
#!/bin/bash
# Buggy pipeline

cat > /tmp/shared_buffer.txt

# Infinite loop
while [ 1 ]; do
    sleep 1
done
EOF
    chmod +x /home/user/buggy_pipeline.sh

    # Create architecture image
    convert -size 800x200 xc:white -pointsize 24 -fill black -draw "text 10,50 'TRANSACTION DELIMITER: TERMINATE_TRANSACTION_99X'" /app/architecture.png

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user