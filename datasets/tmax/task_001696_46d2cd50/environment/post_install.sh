apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        tesseract-ocr \
        imagemagick \
        socat \
        jq \
        netcat-openbsd \
        bsdmainutils \
        gawk \
        fonts-liberation

    pip3 install pytest

    mkdir -p /app/archive_data/set_A /app/archive_data/set_B

    # Valid chunks (Magic: 42 41 4B 01)
    /usr/bin/printf '\x42\x41\x4B\x01\x99\x88\x77' > /app/archive_data/set_A/chunk1.dat
    /usr/bin/printf '\x42\x41\x4B\x01\x11\x22\x33' > /app/archive_data/set_B/chunk3.dat

    # Invalid chunks
    /usr/bin/printf '\x00\x00\x00\x00\x99\x88\x77' > /app/archive_data/set_A/chunk2.dat
    /usr/bin/printf '\x42\x41\x4B\x02\x11\x22\x33' > /app/archive_data/set_B/chunk4.dat

    # Metadata CSV
    cat << 'EOF' > /app/archive_data/index.csv
filename,owner,timestamp
chunk1.dat,admin,2023-10-01T12:00:00Z
chunk2.dat,user1,2023-10-02T12:00:00Z
chunk3.dat,admin,2023-10-03T12:00:00Z
chunk4.dat,user2,2023-10-04T12:00:00Z
EOF

    # Setup for the image fixture
    convert -background white -fill black -pointsize 24 label:"ARCHIVE_X77B9_SECURE" /app/auth_label.png

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user