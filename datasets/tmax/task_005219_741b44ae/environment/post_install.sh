apt-get update && apt-get install -y python3 python3-pip espeak ffmpeg
    pip3 install pytest

    mkdir -p /app

    espeak -w /app/rules.wav "Hello artifact manager. Our path conversion rules are as follows. Read absolute paths from standard input. Ignore any line containing the word 'beta'. For the remaining lines, extract just the file name, removing the directory path. Then, replace all instances of 'arm64' with 'aarch64'. Finally, change the file extension at the end of the filename from '.rar' to '.zip'. For each processed path, print a shell command that first tests the gzip integrity of the original path, and if successful, creates a symbolic link to the original path inside the directory '/curated/' using the newly transformed filename."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user