apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Create the schema image with the required text
    convert -size 600x100 xc:white -font DejaVu-Sans -pointsize 24 -fill black -annotate +10+50 'NEW_ROUTING_SEQUENCE: 4-2-5-1-3' /app/schema.png

    # Create dummy legacy_router binary
    cat << 'EOF' > /app/legacy_router
#!/bin/bash
echo "Legacy router output"
EOF
    chmod +x /app/legacy_router

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app