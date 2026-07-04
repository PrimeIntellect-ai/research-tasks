apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        tesseract-ocr \
        imagemagick \
        fonts-dejavu-core

    pip3 install pytest

    # Create the app directory
    mkdir -p /app

    # Generate the image with the secret prefix
    convert -size 300x100 xc:white -pointsize 24 -fill black -draw "text 20,50 'PREFIX=AERO_V7_'" /app/policy.png

    # Create the user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user