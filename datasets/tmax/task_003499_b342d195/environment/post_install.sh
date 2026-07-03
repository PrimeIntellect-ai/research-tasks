apt-get update && apt-get install -y python3 python3-pip ffmpeg cron
pip3 install pytest

mkdir -p /app
mkdir -p /home/user

python3 -c '
with open("/tmp/subs.srt", "wb") as f:
    f.write(b"1\n00:00:00,000 --> 00:00:01,000\n1710000000|System started normally\n\n")
    f.write(b"2\n00:00:01,000 --> 00:00:02,000\n1710001800|User connected: \xc3\xa9l\xc3\xa8ve\n\n")
    f.write(b"3\n00:00:02,000 --> 00:00:03,000\n1710004000|Error 0xFA \xff\xff\n\n")
'

ffmpeg -f lavfi -i color=c=black:s=320x240:d=3 -i /tmp/subs.srt -c:v libx264 -c:s mov_text /app/telemetry.mp4

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user