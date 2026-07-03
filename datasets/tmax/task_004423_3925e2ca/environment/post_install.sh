apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        golang \
        tesseract-ocr \
        imagemagick \
        fonts-liberation

    pip3 install pytest

    # Create directories
    mkdir -p /app/calibrations
    mkdir -p /app/sim

    # Generate the calibration image
    convert -size 200x150 xc:white -fill black -pointsize 24 -annotate +10+30 "CA: 1.25\nC: 0.85\nN: 1.10" /app/calibrations/weights.png

    # Create user
    useradd -m -s /bin/bash user || true

    # Set permissions
    chmod -R 777 /app
    chmod -R 777 /home/user