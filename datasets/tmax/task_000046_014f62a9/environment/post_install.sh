apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ffmpeg fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Generate the video fixture quickly using ultrafast preset
    ffmpeg -f lavfi -i color=c=black:s=640x480:d=10 -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='KEY\: A1 B2 C3 D4':fontcolor=white:fontsize=24:x=W-tw-10:y=H-th-10:enable='between(t,4.9,5.1)'" -c:v libx264 -preset ultrafast /app/telemetry_feed.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user