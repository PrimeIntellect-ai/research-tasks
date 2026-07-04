apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        tesseract-ocr \
        imagemagick \
        fonts-dejavu-core

    pip3 install pytest

    mkdir -p /app/messy_project/src
    mkdir -p /app/messy_project/logs
    mkdir -p /app/messy_project/docs

    # Generate the instruction image
    convert -size 1000x200 xc:white -font DejaVu-Sans -pointsize 20 -fill black -annotate +10+50 "UPDATE SPECS: Find all .log files. Replace 'OLD_API_KEY_992' with 'SECURE_KEY_7741_VX'." /app/instructions.png

    # Generate dummy files and inject target strings
    python3 -c "
import os
import random

extensions = ['.txt', '.py', '.md', '.log']
subdirs = ['src', 'logs', 'docs']

log_files = []
for i in range(100):
    if i < 20:
        ext = '.log'
        subdir = 'logs'
    else:
        ext = random.choice(extensions)
        subdir = random.choice(subdirs)

    filepath = f'/app/messy_project/{subdir}/file_{i}{ext}'
    with open(filepath, 'w') as f:
        f.write(f'Dummy content for file {i}\n' * 10)

    if ext == '.log':
        log_files.append(filepath)

target_files = random.sample(log_files, 10)
for filepath in target_files:
    with open(filepath, 'a') as f:
        f.write('\nOLD_API_KEY_992\n')
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user