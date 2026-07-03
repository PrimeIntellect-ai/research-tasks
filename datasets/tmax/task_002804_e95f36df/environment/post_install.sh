apt-get update && apt-get install -y python3 python3-pip rustc cargo ffmpeg sox wget tar
    pip3 install --default-timeout=100 pytest numpy scipy

    mkdir -p /app
    mkdir -p /tmp/build

    # Generate a dummy audio file (60 seconds)
    ffmpeg -f lavfi -i "sine=frequency=440:duration=60" -c:a pcm_s16le -ar 44100 /tmp/build/admin_memo.wav

    # Generate the log file in UTF-16LE
    cat << 'EOF' > /tmp/build/storage_audit.txt
[EVENT]
ID: 994
Type: FileSystem
Action: Clean
[/EVENT]
[EVENT]
ID: 995
Type: AudioMemo
KeepStart: 12.50
KeepEnd: 18.25
[/EVENT]
EOF
    iconv -f UTF-8 -t UTF-16LE /tmp/build/storage_audit.txt > /tmp/build/storage_audit.log

    # Create the tar.gz archive
    cd /tmp/build
    tar -czvf /app/legacy_backup.tar.gz admin_memo.wav storage_audit.log

    # Generate the reference trimmed audio
    ffmpeg -i admin_memo.wav -ss 12.50 -to 18.25 -c copy /tmp/reference_memo.wav

    # Clean up build dir
    cd /
    rm -rf /tmp/build

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user