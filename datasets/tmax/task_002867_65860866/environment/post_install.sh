apt-get update && apt-get install -y python3 python3-pip tesseract-ocr bc imagemagick
    pip3 install pytest

    # Create /app directory
    mkdir -p /app

    # Generate the baseline image
    convert -size 200x100 xc:white -fill black -pointsize 36 -annotate +20+60 '150.25' /app/baseline_target.png

    # Create user
    useradd -m -s /bin/bash user || true

    chmod -R 777 /home/user