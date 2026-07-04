apt-get update && apt-get install -y python3 python3-pip ffmpeg zip unzip tar
    pip3 install pytest opencv-python-headless scikit-image

    mkdir -p /app/dataset/frames
    mkdir -p /app/dataset/curated
    mkdir -p /app/.hidden_truth/frames/
    mkdir -p /tmp/setup_data

    # Generate a dummy video for the experiment
    ffmpeg -f lavfi -i testsrc=duration=20:size=640x480:rate=30 -c:v libx264 /app/experiment.mp4

    cd /tmp/setup_data

    # Create telemetry.bin
    echo -n "PHYS_EXP_V01" > telemetry.bin
    # Offset for payload: 12 (header) + 4 (int) + 16 (padding) = 32
    # 32 in 32-bit little endian is \x20\x00\x00\x00
    printf "\x20\x00\x00\x00" >> telemetry.bin
    # Add 16 bytes of garbage padding
    echo -n "GARBAGE_PADDING_" >> telemetry.bin

    # Add payload
    cat << 'EOF' >> telemetry.bin
INFO Booting sensors...
DEBUG Calibration standard.
[CRITICAL] EVENT_TRIGGERED at T=1.50s
WARNING minor temperature fluctuation.
[CRITICAL] EVENT_TRIGGERED at T=5.25s
DEBUG Memory check OK.
[CRITICAL] EVENT_TRIGGERED at T=12.10s
[CRITICAL] EVENT_TRIGGERED at T=15.00s
EOF

    # Package it up
    zip sensor_group_A.zip telemetry.bin
    zip sensor_group_B.zip telemetry.bin
    tar -czvf /app/sensors.tar.gz sensor_group_A.zip sensor_group_B.zip

    # Create hidden truth frames from the generated video
    ffmpeg -ss 1.50 -i /app/experiment.mp4 -frames:v 1 -q:v 2 /app/.hidden_truth/frames/frame_1.50.jpg
    ffmpeg -ss 5.25 -i /app/experiment.mp4 -frames:v 1 -q:v 2 /app/.hidden_truth/frames/frame_5.25.jpg
    ffmpeg -ss 12.10 -i /app/experiment.mp4 -frames:v 1 -q:v 2 /app/.hidden_truth/frames/frame_12.10.jpg
    ffmpeg -ss 15.00 -i /app/experiment.mp4 -frames:v 1 -q:v 2 /app/.hidden_truth/frames/frame_15.00.jpg

    # Cleanup temp setup data
    rm -rf /tmp/setup_data

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user