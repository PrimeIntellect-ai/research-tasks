apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest

    mkdir -p /app
    ffmpeg -f lavfi -i "sine=frequency=440:duration=10" -ac 2 -ar 44100 /app/recording.wav -y

    cat << 'EOF' > /app/oracle_router
#!/bin/bash
X=$1
Y=$2
Z=$3

if [ "$X" -gt 24000 ]; then
    if [ "$Y" -eq 2 ]; then
        echo "high_stereo_$((Z % 10))"
    else
        echo "high_mono_$((Z % 5))"
    fi
else
    if [ "$Y" -eq 2 ]; then
        echo "low_stereo_$((Z % 10))"
    else
        echo "low_mono_$((Z % 5))"
    fi
fi
EOF
    chmod +x /app/oracle_router

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user