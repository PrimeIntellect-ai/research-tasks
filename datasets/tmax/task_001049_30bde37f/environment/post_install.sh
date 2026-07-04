apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        tesseract-ocr \
        imagemagick \
        fonts-dejavu \
        rustc \
        cargo

    pip3 install pytest pandas numpy

    mkdir -p /app/data

    cat << 'EOF' > /app/data/raw_vitals.csv
timestamp,patient_name,heart_rate,temperature
1600000000000,John Doe,72.0,98.6
1600000001500,John Doe,74.5,98.7
1600000003000,John Doe,71.0,98.65
1600000000000,Jane Smith,80.0,99.1
1600000002000,Jane Smith,82.0,99.3
1600000004500,Jane Smith,79.0,99.0
EOF

    convert -size 600x200 xc:white -font DejaVu-Sans -pointsize 18 -fill black -annotate +20+40 "John Doe : 550e8400-e29b-41d4-a716-446655440000\nJane Smith : 123e4567-e89b-12d3-a456-426614174000\nAlice Jones : 987e6543-e21b-34d4-b890-426614174111" /app/config_scan.png

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user