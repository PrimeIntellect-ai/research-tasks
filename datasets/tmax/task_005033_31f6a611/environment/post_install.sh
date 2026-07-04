apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        tesseract-ocr \
        libtesseract-dev \
        cargo \
        rustc \
        build-essential

    pip3 install pytest

    mkdir -p /app/corpus/clean
    mkdir -p /app/corpus/evil
    mkdir -p /app/hidden_corpus/clean
    mkdir -p /app/hidden_corpus/evil

    # Create dummy files for corpus to prevent empty directory issues
    echo "COPY users TO '/mnt/backups/users.csv';" > /app/corpus/clean/sample1.sql
    echo "COPY users TO '/tmp/users.csv';" > /app/corpus/evil/sample1.sql
    echo "COPY logs TO '/mnt/backups/logs.csv';" > /app/hidden_corpus/clean/sample1.sql
    echo "COPY logs TO '/var/www/html/logs.csv';" > /app/hidden_corpus/evil/sample1.sql

    # Create a dummy video file
    touch /app/dashboard.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app